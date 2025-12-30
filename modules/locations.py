
# Dictionary of Countries and Major Cities with Coordinates (Lat, Lon)
# Focused on China (major cities) and key global hubs.

LOCATIONS = {
    "中国 (China)": {
        "北京 (Beijing)": (39.9042, 116.4074),
        "上海 (Shanghai)": (31.2304, 121.4737),
        "广州 (Guangzhou)": (23.1291, 113.2644),
        "深圳 (Shenzhen)": (22.5431, 114.0579),
        "成都 (Chengdu)": (30.5728, 104.0668),
        "杭州 (Hangzhou)": (30.2741, 120.1551),
        "武汉 (Wuhan)": (30.5928, 114.3055),
        "重庆 (Chongqing)": (29.5630, 106.5516),
        "南京 (Nanjing)": (32.0603, 118.7969),
        "天津 (Tianjin)": (39.0842, 117.2009),
        "西安 (Xi'an)": (34.3416, 108.9398),
        "苏州 (Suzhou)": (31.2989, 120.5853),
        "郑州 (Zhengzhou)": (34.7466, 113.6253),
        "长沙 (Changsha)": (28.2282, 112.9388),
        "沈阳 (Shenyang)": (41.8057, 123.4315),
        "青岛 (Qingdao)": (36.0671, 120.3826),
        "大连 (Dalian)": (38.9140, 121.6147),
        "厦门 (Xiamen)": (24.4798, 118.0894),
        "昆明 (Kunming)": (24.8801, 102.8329),
        "福州 (Fuzhou)": (26.0745, 119.2965),
        "哈尔滨 (Harbin)": (45.8038, 126.5349),
        "济南 (Jinan)": (36.6512, 117.1201),
        "长春 (Changchun)": (43.8171, 125.3235),
        "南宁 (Nanning)": (22.8170, 108.3665),
        "太原 (Taiyuan)": (37.8706, 112.5489),
        "合肥 (Hefei)": (31.8206, 117.2272),
        "贵阳 (Guiyang)": (26.6470, 106.6302),
        "乌鲁木齐 (Urumqi)": (43.8256, 87.6168),
        "兰州 (Lanzhou)": (36.0611, 103.8343),
        "海口 (Haikou)": (20.0174, 110.3492),
        "香港 (Hong Kong)": (22.3193, 114.1694),
        "澳门 (Macau)": (22.1987, 113.5439),
        "台北 (Taipei)": (25.0330, 121.5654)
    },
    "美国 (USA)": {
        "New York": (40.7128, -74.0060),
        "Los Angeles": (34.0522, -118.2437),
        "Chicago": (41.8781, -87.6298),
        "San Francisco": (37.7749, -122.4194),
        "Washington D.C.": (38.9072, -77.0369),
        "Seattle": (47.6062, -122.3321),
        "Boston": (42.3601, -71.0589)
    },
    "英国 (UK)": {
        "London": (51.5074, -0.1278),
        "Manchester": (53.4808, -2.2426),
        "Edinburgh": (55.9533, -3.1883)
    },
    "日本 (Japan)": {
        "Tokyo": (35.6762, 139.6503),
        "Osaka": (34.6937, 135.5023),
        "Kyoto": (35.0116, 135.7681)
    },
    "加拿大 (Canada)": {
        "Toronto": (43.6510, -79.3470),
        "Vancouver": (49.2827, -123.1207),
        "Montreal": (45.5017, -73.5673)
    },
    "澳大利亚 (Australia)": {
        "Sydney": (-33.8688, 151.2093),
        "Melbourne": (-37.8136, 144.9631)
    },
    "德国 (Germany)": {
        "Berlin": (52.5200, 13.4050),
        "Munich": (48.1351, 11.5820),
        "Frankfurt": (50.1109, 8.6821)
    },
    "法国 (France)": {
        "Paris": (48.8566, 2.3522)
    },
    "新加坡 (Singapore)": {
        "Singapore": (1.3521, 103.8198)
    }
}

def get_coordinates(country, city):
    """
    Returns (lat, lon) tuple for a given country and city.
    Defaults to Beijing if not found.
    """
    try:
        return LOCATIONS[country][city]
    except KeyError:
        return (39.9042, 116.4074) # Default Beijing
