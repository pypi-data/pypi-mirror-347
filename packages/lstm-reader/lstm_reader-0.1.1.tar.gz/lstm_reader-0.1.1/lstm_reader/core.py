# core.py
import pandas as pd
import numpy as np
import torch
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error as mse, mean_absolute_error as mae
import math

class RNN(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super().__init__()
        self.rnn = torch.nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )
        self.out = torch.nn.Linear(hidden_size, output_size)

    def forward(self, x):
        output, _ = self.rnn(x)
        return self.out(output[:, -1, :]), None


def read_train(
    csv_path: str,
    station_id: int,
    save_model_path: str,
    window_length: int = 8,
    pre_length: int = 8,
    hidden_size: int = 16,
    num_layers: int = 4,
    lr: float = 0.01,
    epochs: int = 100,
    batch_size: int = 32,
    device: str = 'cpu',
):
    """
    读取 csv，训练 LSTM 模型并保存到 save_model_path。
    """
    # 1. 读取与筛选
    data = pd.read_csv(csv_path)
    data['ENTRY_DATETIME'] = pd.to_datetime(data['ENTRY_DATETIME'])
    series = data[data['LINE_STATION'] == station_id]['COUNT'].values.astype(float)

    # 2. 归一化
    scaler = MinMaxScaler((0,1))
    scaled = scaler.fit_transform(series.reshape(-1,1)).flatten()

    # 3. 构造样本
    x, y = [], []
    for t in range(len(scaled) - pre_length):
        cur = scaled[max(0, t-window_length):t]
        lag = scaled[t-96-window_length:t-96] if t-96-window_length>=0 else None
        if len(cur)==window_length and lag is not None:
            feat = np.stack([cur, lag], axis=1)
            x.append(feat)
            y.append(scaled[t:t+pre_length])
    x = np.array(x); y = np.array(y)

    # 4. 划分训练/测试
    train_size = len(x) - 96*2
    trainX = torch.tensor(x[:train_size], dtype=torch.float32)
    trainY = torch.tensor(y[:train_size], dtype=torch.float32)
    dataset = torch.utils.data.TensorDataset(trainX, trainY)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # 5. 模型、优化器、损失
    model = RNN(x.shape[2], hidden_size, pre_length, num_layers).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.MSELoss()

    # 6. 训练循环
    def mape(a,b): return np.mean(np.abs((a - b)/a)[a>0])*100
    best_mape = float('inf')
    for epoch in range(1, epochs+1):
        for bx, by in loader:
            bx, by = bx.to(device), by.to(device)
            pred, _ = model(bx)
            loss = loss_fn(pred, by)
            optimizer.zero_grad(); loss.backward(); optimizer.step()
        # 可选择添加验证与保存逻辑，此处简化为最终保存
    torch.save(model, save_model_path)
    return save_model_path, scaler


def read_predict(
    model_path: str,
    csv_path: str,
    station_id: int,
    output_path: str,
    window_length: int = 8,
    lag_steps: int = 96,
    device: str = 'cpu',
):
    """
    加载模型，对最新数据做单步预测并保存到 excel。
    """
    # 1. 加载模型
    model = torch.load(model_path, map_location=device)
    model.eval()

    # 2. 读取与归一化
    df = pd.read_csv(csv_path)
    df['ENTRY_DATETIME'] = pd.to_datetime(df['ENTRY_DATETIME'])
    series = df[df['LINE_STATION']==station_id]['COUNT'].values.astype(float)
    scaler = MinMaxScaler((0,1))
    scaled = scaler.fit_transform(series.reshape(-1,1)).flatten()

    # 3. 构造输入
    cur = scaled[-window_length:]
    if len(scaled) >= window_length + lag_steps:
        lag = scaled[-window_length-lag_steps:-lag_steps]
    else:
        lag = scaled[:window_length]
    inp = np.stack([cur, lag], axis=1)[None,...].astype(np.float32)
    inp = torch.tensor(inp).to(device)

    # 4. 预测与反归一
    with torch.no_grad(): pred, _ = model(inp)
    out = scaler.inverse_transform(pred.cpu().numpy())

    # 5. 时间索引与保存
    last_time = df['ENTRY_DATETIME'].iloc[-1]
    idx = [last_time + pd.Timedelta(minutes=15*(i+1)) for i in range(out.shape[1])]
    pd.DataFrame({'ENTRY_DATETIME': idx, 'predicted_in': out.flatten().round().astype(int)})
        .to_excel(output_path, index=False)
    return output_path
