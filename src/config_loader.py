import os

def load_env_file(file_path='.env'):
    """
    .envファイルから設定を読み込む関数
    
    Args:
        file_path: .envファイルのパス
        
    Returns:
        dict: 設定値を格納した辞書
    """
    config = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # コメント行や空行をスキップ
                if not line or line.startswith('#'):
                    continue
                    
                # キーと値を分割
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # 値の型を適切に変換
                    if value.lower() == 'true':
                        config[key] = True
                    elif value.lower() == 'false':
                        config[key] = False
                    elif value.isdigit():
                        config[key] = int(value)
                    else:
                        try:
                            config[key] = float(value)
                        except ValueError:
                            config[key] = value
    except Exception as e:
        print(f"設定ファイルの読み込みエラー: {e}")
        
    return config
