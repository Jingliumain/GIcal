import random
from typing import List, Dict, Optional, Tuple

# 聖遺物の部位
ARTIFACT_POSITIONS = ["花", "羽", "杯", "冠", "時"]

# メインステータスの定義と値
MAIN_STATS = {
    "花": {"HP": 717},  # 固定値
    "羽": {"攻撃力": 47},  # 固定値
    "杯": {
        "HP": 43.57,
        "攻撃力": 43.57,
        "防御力": 54.49,
        "元素ダメージ": 46.6,
        "物理ダメージ": 58.3
    },
    "冠": {
        "HP": 43.57,
        "攻撃力": 43.57,
        "防御力": 54.49,
        "会心率": 31.1,
        "会心ダメージ": 62.2,
        "治癒量": 35.9
    },
    "時": {
        "HP": 43.57,
        "攻撃力": 43.57,
        "防御力": 54.49,
        "元素熟知": 186.5,
        "元素チャージ": 51.8
    }
}

# サブステータスのロール値（各ステータスごとに4段階）
# 最高値 / 0.9倍 / 0.8倍 / 0.7倍
SUBSTAT_ROLLS = {
    "HP": [239.0, 215.1, 191.2, 167.3],
    "攻撃力": [19.45, 17.505, 15.56, 13.615],
    "防御力": [23.15, 20.835, 18.52, 16.205],
    "HP%": [5.83, 5.247, 4.664, 4.081],
    "攻撃力%": [7.29, 6.561, 5.832, 5.103],
    "防御力%": [7.29, 6.561, 5.832, 5.103],
    "元素熟知": [23.31, 20.979, 18.648, 16.317],
    "元素チャージ": [6.48, 5.832, 5.184, 4.536],
    "会心率": [3.89, 3.501, 3.112, 2.723],
    "会心ダメージ": [7.77, 6.993, 6.216, 5.439],
}

# サブステータスの出現確率（画像から抽出）
SUBSTAT_PROBABILITIES = {
    "HP": 13.99,
    "攻撃力": 14.69,
    "防御力": 15.03,
    "HP%": 10.78,
    "攻撃力%": 10.65,
    "防御力%": 10.34,
    "元素熟知": 9.58,
    "元素チャージ": 9.43,
    "会心率": 8.18,
    "会心ダメージ": 7.92,
}


def get_random_roll(stat_name: str) -> float:
    """ランダムなロール値を取得（4段階：1.0, 0.9, 0.8, 0.7倍）"""
    rolls = SUBSTAT_ROLLS[stat_name]
    return random.choice(rolls)


def get_available_substats(main_stat: str) -> Dict[str, float]:
    """メインステータスに基づいて利用可能なサブステータスを取得"""
    # メインステータスをサブステータスから除外
    available = {k: v for k, v in SUBSTAT_PROBABILITIES.items() if k != main_stat}
    
    # 確率の合計で正規化
    total = sum(available.values())
    return {k: v / total for k, v in available.items()}


def generate_main_stat(position: str) -> Tuple[str, float]:
    """メインステータスを生成
    
    Returns:
        (ステータス名, 値)のタプル
    """
    stats = MAIN_STATS[position]
    stat_name = random.choice(list(stats.keys()))
    return stat_name, stats[stat_name]


def generate_substats(main_stat: str, count: int = 4) -> List[Tuple[str, float]]:
    """サブステータスを生成（重複なし）
    
    Args:
        main_stat: メインステータス
        count: 初期サブステータスの数（3 or 4）
    
    Returns:
        [(ステータス名, 値), ...]のリスト
    """
    available = get_available_substats(main_stat)
    
    # 確率に基づいてサブステータスを選択
    substats = []
    available_list = list(available.items())
    
    for _ in range(count):
        if not available_list:
            break
        
        # 確率に基づいて選択
        stats, probs = zip(*available_list)
        chosen = random.choices(stats, weights=probs, k=1)[0]
        
        # ロール値を決定
        roll_value = get_random_roll(chosen)
        substats.append((chosen, roll_value))
        
        # 選択したものを除外
        available_list = [(s, p) for s, p in available_list if s != chosen]
    
    return substats


def upgrade_substats(substats: List[Tuple[str, float]], main_stat: str) -> List[Tuple[str, float]]:
    """サブステータスをレベルアップ時に成長させる
    
    Args:
        substats: 現在のサブステータス
        main_stat: メインステータス（重複チェック用）
    
    Returns:
        成長後のサブステータス
    """
    upgraded = [list(sub) for sub in substats]
    
    for upgrade_count in range(5):
        if len(upgraded) < 4:
            # サブステータスが3つ以下の場合、新しいサブステータスを追加
            available = get_available_substats(main_stat)
            
            # 既存のサブステータスを除外
            existing_stats = {sub[0] for sub in upgraded}
            available = {k: v for k, v in available.items() if k not in existing_stats}
            
            if not available:
                continue
            
            # 正規化
            total = sum(available.values())
            available = {k: v / total for k, v in available.items()}
            
            stats, probs = zip(*available.items())
            chosen = random.choices(stats, weights=probs, k=1)[0]
            
            roll_value = get_random_roll(chosen)
            upgraded.append([chosen, roll_value])
        else:
            # サブステータスが4つの場合、ランダムに1つを選んで成長
            chosen_index = random.randint(0, 3)
            stat_name = upgraded[chosen_index][0]
            
            roll_value = get_random_roll(stat_name)
            upgraded[chosen_index][1] += roll_value
    
    return [(sub[0], round(sub[1], 2)) for sub in upgraded]


def generate_artifact(position: Optional[str] = None) -> Dict:
    """聖遺物を生成
    
    Args:
        position: 聖遺物の部位（"花", "羽", "杯", "冠", "時"）
                 Noneの場合はランダムに選択
    
    Returns:
        聖遺物のデータ辞書
    """
    if position is None:
        position = random.choice(ARTIFACT_POSITIONS)
    elif position not in ARTIFACT_POSITIONS:
        raise ValueError(f"部位は {ARTIFACT_POSITIONS} のいずれかである必要があります")
    
    # メインステータスを生成
    main_stat_name, main_stat_value = generate_main_stat(position)
    
    # 初期サブステータス数（3 or 4）
    initial_substat_count = random.choice([3, 4])
    
    # サブステータスを生成
    substats = generate_substats(main_stat_name, initial_substat_count)
    
    # レベルアップ時にサブステータスを成長
    upgraded_substats = upgrade_substats(substats, main_stat_name)
    
    return {
        "部位": position,
        "メインOP": {
            "名前": main_stat_name,
            "値": main_stat_value
        },
        "サブOP": [
            {
                "名前": sub[0],
                "値": sub[1]
            }
            for sub in upgraded_substats
        ]
    }


def generate_artifacts(count: int, position: Optional[str] = None) -> List[Dict]:
    """複数の聖遺物を生成
    
    Args:
        count: 生成する聖遺物の数
        position: 聖遺物の部位（Noneの場合はランダム）
    
    Returns:
        聖遺物のリスト
    """
    if count < 1:
        raise ValueError("聖遺物の数は1以上である必要があります")
    
    return [generate_artifact(position) for _ in range(count)]


def print_artifacts(artifacts: List[Dict]) -> None:
    """聖遺物を見やすく表示"""
    for i, artifact in enumerate(artifacts, 1):
        print(f"\n聖遺物 #{i}")
        print(f"  部位: {artifact['部位']}")
        main_op = artifact["メインOP"]
        print(f"  メインOP: {main_op['名前']} +{main_op['値']}")
        print(f"  サブOP:")
        for sub_op in artifact["サブOP"]:
            print(f"    - {sub_op['名前']}: +{sub_op['値']}")


# テスト実行
if __name__ == "__main__":
    # 例1: ランダムな部位で5個の聖遺物を生成
    print("=== ランダムな部位で5個生成 ===")
    artifacts = generate_artifacts(5)
    print_artifacts(artifacts)
    
    # 例2: 杯の部位で3個の聖遺物を生成
    print("\n\n=== 杯の部位で3個生成 ===")
    artifacts = generate_artifacts(3, "杯")
    print_artifacts(artifacts)
    
    # 例3: 配列形式で出力
    print("\n\n=== 配列形式で出力 ===")
    artifacts = generate_artifacts(2)
    print(artifacts)