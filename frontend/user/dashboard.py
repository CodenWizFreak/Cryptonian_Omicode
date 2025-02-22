import streamlit as st

def set_style():
    st.markdown("""
        <style>
        /* Base theme */
        .stApp {
            background: #000000;
        }
        
        /* Stats cards */
        .stats-container {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 12px;
            padding: 24px;
            margin: 10px 0;
            border: 1px solid rgba(78, 108, 180, 0.2);
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(96, 165, 250, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .stats-container:hover {
            transform: translateY(-4px);
            border-color: #60a5fa;
            box-shadow: 0 8px 25px rgba(96, 165, 250, 0.2);
        }
        
        .stats-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #60a5fa, #93c5fd);
            box-shadow: 0 0 20px rgba(96, 165, 250, 0.5);
        }
        
        .stats-value {
            font-size: 36px;
            font-weight: bold;
            background: linear-gradient(90deg, #60a5fa, #93c5fd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            text-shadow: 0 0 20px rgba(96, 165, 250, 0.3);
        }
        
        .stats-label {
            color: #94a3b8;
            font-size: 16px;
            font-weight: 500;
        }
        
        /* Achievement cards */
        .achievement-card {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(78, 108, 180, 0.2);
            transition: all 0.3s ease;
        }
        
        .achievement-card:hover {
            transform: translateY(-4px);
            border-color: #60a5fa;
            box-shadow: 0 8px 25px rgba(96, 165, 250, 0.2);
        }
        
        .achievement-title {
            color: #f8fafc;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .achievement-desc {
            color: #94a3b8;
            font-size: 0.9rem;
            margin-top: 8px;
        }
        
        /* Progress bars */
        .progress-container {
            background: rgba(51, 65, 85, 0.4);
            border-radius: 8px;
            height: 8px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #60a5fa, #93c5fd);
            border-radius: 8px;
            transition: width 0.6s ease;
            box-shadow: 0 0 10px rgba(96, 165, 250, 0.3);
        }
        
        /* Certificate cards */
        .certificate-card {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(78, 108, 180, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }
        
        .certificate-card:hover {
            transform: translateY(-4px);
            border-color: #60a5fa;
            box-shadow: 0 8px 25px rgba(96, 165, 250, 0.2);
        }
        
        .certificate-info {
            flex-grow: 1;
        }
        
        .certificate-title {
            color: #f8fafc;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .certificate-status {
            color: #94a3b8;
            font-size: 0.9rem;
        }
        
        .btn-action {
            background: rgba(96, 165, 250, 0.2);
            color: #60a5fa;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-left: 16px;
            box-shadow: 0 0 15px rgba(96, 165, 250, 0.1);
        }
        
        .btn-action:hover {
            background: rgba(96, 165, 250, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 0 20px rgba(96, 165, 250, 0.2);
        }
        
        /* Section headers */
        .section-header {
            color: #f8fafc;
            font-size: 1.5rem;
            font-weight: 600;
            margin: 24px 0 16px 0;
            text-shadow: 0 0 20px rgba(96, 165, 250, 0.2);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.6);
        }
        
        ::-webkit-scrollbar-thumb {
            background: #60a5fa;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #93c5fd;
        }
        </style>
    """, unsafe_allow_html=True)

def render_stat(value, label):
    st.markdown(f"""
        <div class="stats-container">
            <div class="stats-value">{value}</div>
            <div class="stats-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)

def render_achievement(title, progress, description):
    st.markdown(f"""
        <div class="achievement-card">
            <div class="achievement-title">{title}</div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%"></div>
            </div>
            <div class="achievement-desc">{description}</div>
        </div>
    """, unsafe_allow_html=True)

def render_certificate(name, status, action=None):
    action_button = f'<button class="btn-action">{action}</button>' if action else ''
    st.markdown(f"""
        <div class="certificate-card">
            <div class="certificate-info">
                <div class="certificate-title">{name}</div>
                <div class="certificate-status">{status}</div>
            </div>
            {action_button}
        </div>
    """, unsafe_allow_html=True)

def render_dashboard(wallet_address):
    st.title("Learning Dashboard")
    
    # Stats Section
    st.markdown('<div class="section-header">Statistics</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    stats = [
        {"value": "15", "label": "Lessons Complete"},
        {"value": "8", "label": "Games Won"},
        {"value": "3", "label": "NFTs Earned"}
    ]
    
    for col, stat in zip(cols, stats):
        with col:
            render_stat(stat["value"], stat["label"])
    
    # Achievements Section
    st.markdown('<div class="section-header">Achievements</div>', unsafe_allow_html=True)
    achievements = [
        {
            "title": "Web3 Novice",
            "progress": 100,
            "description": "Completed first Web3 lesson"
        },
        {
            "title": "Geography Explorer",
            "progress": 60,
            "description": "Visit 5 monuments"
        },
        {
            "title": "History Master",
            "progress": 40,
            "description": "Complete all history lessons"
        },
        {
            "title": "NFT Collector",
            "progress": 40,
            "description": "Collect 5 NFTs"
        }
    ]
    
    cols = st.columns(2)
    for idx, achievement in enumerate(achievements):
        with cols[idx % 2]:
            render_achievement(
                achievement["title"],
                achievement["progress"],
                achievement["description"]
            )
    
    # Certificates Section
    st.markdown('<div class="section-header">Certificates</div>', unsafe_allow_html=True)
    certificates = [
        {
            "name": "Web3 Fundamentals",
            "status": "Completed",
            "action": "Mint Certificate"
        },
        {
            "name": "Geography Explorer",
            "status": "In Progress",
            "action": "Download"
        },
        {
            "name": "History Scholar",
            "status": "65% Complete",
            "action": None
        }
    ]
    
    for cert in certificates:
        render_certificate(
            cert["name"],
            cert["status"],
            cert.get("action")
        )

def app(wallet_address):
    set_style()
    render_dashboard(wallet_address)
