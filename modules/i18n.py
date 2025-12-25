
TRANSLATIONS = {
    "CN": {
        "title": "熵之神",
        "splash_logo_missing": "[图标丢失]",
        "splash_title": "熵 之 神",
        "splash_subtitle": "// 系统唤醒中 //",
        "splash_init_btn": ">>> 初始化系统 <<<",
        "loading_modules": "加载核心模块...",
        
        "cal_title": "// 身份锚点校准",
        "cal_meta_label": "身份元数据 (必填)",
        "cal_name_label": "代号 (姓名)",
        "cal_phone_label": "通讯链路 (手机号)",
        "cal_date_label": "初始日期 (生日)",
        "cal_btn": "建立连接",
        "cal_error_missing": "数据缺失。请补全所有字段。",
        "cal_syncing": "同步生物哈希值...",
        
        "rad_connected": "已连接",
        "rad_entropy_state": "熵状态",
        "rad_east_title": "东方矢量",
        "rad_day_master": "日主",
        "rad_animal": "生肖",
        "rad_west_title": "西方矢量",
        "rad_sun": "太阳星座",
        "rad_moon": "月亮星座",
        "rad_tab_void": "虚空询问",
        "rad_tab_lens": "透镜预言",
        
        "void_input_label": "目标变量 (选填)",
        "void_input_placeholder": "留空以获取今日综合运势分析",
        "void_btn": "询问虚空",
        "void_default_query": "关于系统稳定性和熵值的今日综合分析。",
        "void_processing": "计算中...",
        "void_aligning": "正在对齐",
        "void_compensating": "正在补偿局部混乱指数...",
        "void_complete": "传输接收完成",
        "void_error_conn": "连接失败",
        
        "lens_info": "上传物品以进行分析 (物体预言)",
        "lens_cam_label": "扫描物体",
        "lens_btn": "分析造物",
        "lens_processing": "视觉皮层已介入...",
        
        "rev_title": "// 熵减报告 //",
        "rev_ack_btn": "确认知晓"
    },
    "EN": {
        "title": "Entropy God",
        "splash_logo_missing": "[LOGO MISSING]",
        "splash_title": "ENTROPY GOD",
        "splash_subtitle": "// SYSTEM AWAKENING //",
        "splash_init_btn": ">>> INITIALIZE SYSTEM <<<",
        "loading_modules": "LOADING CORE MODULES...",
        
        "cal_title": "// IDENTITY CALIBRATION",
        "cal_meta_label": "IDENTITY METADATA (Required)",
        "cal_name_label": "DESIGNATION (Name)",
        "cal_phone_label": "COMM LINK (Phone)",
        "cal_date_label": "INCEPTION DATE (Birthday)",
        "cal_btn": "ESTABLISH CONNECTION",
        "cal_error_missing": "DATA FRAGMENTED. PLEASE COMPLETE ALL FIELDS.",
        "cal_syncing": "SYNCING BIOMETRIC HASH...",
        
        "rad_connected": "CONNECTED",
        "rad_entropy_state": "ENTROPY STATE",
        "rad_east_title": "EASTERN VECTOR",
        "rad_day_master": "DAY MASTER",
        "rad_animal": "ANIMAL",
        "rad_west_title": "WESTERN VECTOR",
        "rad_sun": "SUN SIGN",
        "rad_moon": "MOON SIGN",
        "rad_tab_void": "VOID QUERY",
        "rad_tab_lens": "LENS PROPHECY",
        
        "void_input_label": "TARGET VARIABLE (Optional)",
        "void_input_placeholder": "Leave empty for General Daily Analysis",
        "void_btn": "QUERY THE VOID",
        "void_default_query": "General Daily Analysis regarding stability and entropy.",
        "void_processing": "PROCESSING...",
        "void_aligning": "Aligning",
        "void_compensating": "Compensating for local chaos index...",
        "void_complete": "TRANSMISSION RECEIVED",
        "void_error_conn": "CONNECTION FAILED",
        
        "lens_info": "UPLOAD ARTIFACT FOR ANALYSIS (Object Prophecy)",
        "lens_cam_label": "SCAN OBJECT",
        "lens_btn": "ANALYZE ARTIFACT",
        "lens_processing": "VISUAL CORTEX ENGAGED...",
        
        "rev_title": "// ENTROPY REDUCTION REPORT //",
        "rev_ack_btn": "ACKNOWLEDGE"
    }
}

def get_text(key, lang="CN"):
    return TRANSLATIONS.get(lang, TRANSLATIONS["CN"]).get(key, f"[{key}]")
