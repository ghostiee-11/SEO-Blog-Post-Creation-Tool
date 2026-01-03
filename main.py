import streamlit as st
from scrapers.amazon import search_amazon
from scrapers.ebay import search_ebay, get_ebay_details
from agents.seo_agent import generate_seo_strategy
from agents.writer_agent import write_blog_post
from publishers.wordpress import publish_to_wordpress

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI SEO Blog Tool", layout="wide")

# --- CSS STYLES ---
st.markdown("""
<style>
    .product-card { border: 1px solid #e0e0e0; padding: 15px; border-radius: 10px; background: white; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .price-tag { color: #2e7d32; font-weight: bold; font-size: 1.1em; background: #e8f5e9; padding: 2px 8px; border-radius: 4px; }
    .bestseller-btn { width: 100%; border: 2px solid #FF9900; color: #FF9900; }
    .success-msg { background-color: #d1e7dd; color: #0f5132; padding: 10px; border-radius: 5px; margin-top: 10px;}
</style>
""", unsafe_allow_html=True)

st.title("AI SEO Blog Creator")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("⚙️ Configuration")
    platform = st.radio("Select Source:", ["eBay", "Amazon"], help="Switch between eBay Global Deals and Amazon Best Sellers.")
    st.divider()
    
    # NEW: Quick Action Button in Sidebar
    st.markdown("### ⚡ Quick Actions")
    if st.button("🔥 Get Top Bestsellers", type="primary", use_container_width=True):
        with st.spinner(f"Scraping {platform} Top Charts..."):
            # Passing None or empty string triggers the 'Bestsellers' logic in the scraper
            if platform == "eBay":
                st.session_state.results = search_ebay(None)
            else:
                st.session_state.results = search_amazon(None)
            st.session_state.selected_prod = None
            st.session_state.blog_content = None

# --- SESSION STATE ---
if "results" not in st.session_state: st.session_state.results = []
if "selected_prod" not in st.session_state: st.session_state.selected_prod = None
if "blog_content" not in st.session_state: st.session_state.blog_content = None
if "seo_data" not in st.session_state: st.session_state.seo_data = None

# --- SEARCH AREA ---
st.markdown(f"### Find Products on **{platform}**")
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input("Search Keyword", placeholder="e.g. Mechanical Keyboard, Yoga Mat...")
with col2:
    st.write("") 
    st.write("") 
    if st.button("🔍 Search", use_container_width=True):
        if query:
            with st.spinner(f"Searching {platform} for '{query}'..."):
                if platform == "eBay":
                    st.session_state.results = search_ebay(query)
                else:
                    st.session_state.results = search_amazon(query)
                st.session_state.selected_prod = None
                st.session_state.blog_content = None
        else:
            st.warning("Please enter a keyword first.")

# --- RESULTS GRID ---
if st.session_state.results:
    st.divider()
    st.subheader(f"Found {len(st.session_state.results)} Products")
    
    # Dynamic Grid (4 items per row)
    cols = st.columns(4)
    for idx, prod in enumerate(st.session_state.results):
        with cols[idx % 4]:
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <img src="{prod.get('image', '')}" style="width:100%; height:150px; object-fit:contain; margin-bottom:10px;">
                    <div style="height: 50px; overflow: hidden; font-weight: bold;">{prod['title'][:50]}...</div>
                    <div style="margin-top: 10px;">
                        <span class="price-tag">{prod['price']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("✨ Write Blog", key=f"btn_{idx}", use_container_width=True):
                    st.session_state.selected_prod = prod
                    st.session_state.blog_content = None
                    st.rerun()

# --- BLOG GENERATION & PUBLISHING ---
if st.session_state.selected_prod:
    prod = st.session_state.selected_prod
    st.divider()
    st.subheader("📝 AI Content Studio")
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.image(prod['image'], use_container_width=True)
        st.info(f"**Selected:** {prod['title']}")
        st.caption(f"Source: {prod['source']}")

    with c2:
        # Step 1: Generate
        if not st.session_state.blog_content:
            with st.status("🤖 AI Agents Working...", expanded=True):
                st.write("🔍 Deep-diving product details...")
                details = get_ebay_details(prod['url']) if platform == "eBay" else prod['title']
                
                st.write("🧠 Researching SEO keywords (Llama-3)...")
                seo = generate_seo_strategy(prod['title'], details)
                st.session_state.seo_data = seo
                
                if seo:
                    st.write("✍️ Writing optimized article...")
                    blog = write_blog_post(prod, seo, details)
                    st.session_state.blog_content = blog
                    st.rerun()
                else:
                    st.error("AI failed. Try another product.")

        # Step 2: Review & Publish
        else:
            tab1, tab2 = st.tabs(["📄 Preview", "💻 Markdown"])
            with tab1:
                st.markdown(st.session_state.blog_content)
            with tab2:
                st.code(st.session_state.blog_content, language="markdown")
            
            st.divider()
            
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.download_button("📥 Download File", st.session_state.blog_content, "blog.md", use_container_width=True)
            
            with p_col2:
                if st.button("🚀 Publish to WordPress", type="primary", use_container_width=True):
                    with st.spinner("Posting..."):
                        tags = st.session_state.seo_data.get('secondary_keywords', [])
                        res = publish_to_wordpress(f"Review: {prod['title']}", st.session_state.blog_content, tags, prod['url'])
                        
                        if res['success']:
                            st.markdown(f"<div class='success-msg'>✅ Published! <a href='{res['link']}' target='_blank'>View Post</a></div>", unsafe_allow_html=True)
                        else:
                            st.error(f"Error: {res['error']}")