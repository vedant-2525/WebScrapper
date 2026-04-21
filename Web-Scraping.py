# Importing Required Libraries

# For Frontend(Provides Interface) and Deployment
import streamlit as st

# requests is used to get access to the website or in other words connect to the website
import requests

# Beautiful Soup 4 is a Python library that makes it easy to scrape information from web pages.
# It provides Pythonic idioms for iterating, searching, and modifying the parse tree.
# The library sits atop an HTML or XML parser.
from bs4 import BeautifulSoup

# For Reading PDF Files and Manipulation in PDF Files
import PyPDF2

# For Reading PDF Files Bytes by Bytes Instead of Downloading them
from io import BytesIO

# For Parsing and Joining Links
from urllib.parse import urlparse, urljoin

# For Rendering in Zip File
import zipfile

# For File Operations
import os

# Consistent Zipfile Naming
ZIP_PDF_FILENAME = "Zip_File_PDF.zip"
ZIP_IMAGE_FILENAME = "Zip_File_Image.zip"

# Adding Variables for Visited Links so that we do not visit them again while scraping
visited_links = []

# Set a maximum size for the zip file in bytes
MAX_ZIP_FILE_SIZE = 1024 * 1024 * 100  # 100 MB


# ─────────────────────────────────────────────
# CUSTOM CSS — Dark Theme + Glassmorphism
# ─────────────────────────────────────────────
def inject_custom_css():
    st.markdown(
        """
        <style>
        /* ── Google Font ── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ── Root variables ── */
        :root {
            --bg-primary: #0a0a1a;
            --bg-secondary: #12122a;
            --bg-card: rgba(255, 255, 255, 0.04);
            --bg-card-hover: rgba(255, 255, 255, 0.07);
            --border-card: rgba(255, 255, 255, 0.08);
            --text-primary: #e8e8f0;
            --text-secondary: #9898b8;
            --text-muted: #6868a0;
            --accent-1: #6c63ff;
            --accent-2: #00d4aa;
            --accent-gradient: linear-gradient(135deg, #6c63ff, #00d4aa);
            --danger: #ff4d6a;
            --warning: #ffb84d;
            --success: #00d4aa;
            --radius: 16px;
            --radius-sm: 10px;
            --shadow-glow: 0 0 30px rgba(108, 99, 255, 0.15);
        }

        /* ── Global resets ── */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background: var(--bg-primary) !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: var(--bg-secondary) !important;
            border-right: 1px solid var(--border-card) !important;
        }

        [data-testid="stSidebar"] * {
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stRadio label {
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
        }

        /* ── Animated gradient bar at top ── */
        [data-testid="stApp"]::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--accent-gradient);
            background-size: 200% 200%;
            animation: gradientShift 4s ease infinite;
            z-index: 9999;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* ── Headings ── */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
        }

        /* ── Glass Card blocks (st.container, expander, etc) ── */
        [data-testid="stExpander"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-card) !important;
            border-radius: var(--radius) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        [data-testid="stExpander"]:hover {
            background: var(--bg-card-hover) !important;
            border-color: rgba(108, 99, 255, 0.25) !important;
            box-shadow: var(--shadow-glow);
        }

        [data-testid="stExpander"] summary {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
        }

        /* ── Text Input ── */
        .stTextInput > div > div > input {
            background: rgba(20, 20, 45, 0.9) !important;
            border: 1px solid var(--border-card) !important;
            border-radius: var(--radius-sm) !important;
            color: #ffffff !important;
            caret-color: #ffffff !important;
            padding: 12px 16px !important;
            font-size: 0.95rem !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease;
            -webkit-text-fill-color: #ffffff !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: var(--accent-1) !important;
            box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.25) !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: var(--text-muted) !important;
            -webkit-text-fill-color: var(--text-muted) !important;
        }

        .stTextInput label {
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }

        /* ── Select box ── */
        .stSelectbox > div > div {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-card) !important;
            border-radius: var(--radius-sm) !important;
            color: var(--text-primary) !important;
        }

        .stSelectbox label {
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
        }

        [data-baseweb="select"] {
            background: var(--bg-card) !important;
        }

        [data-baseweb="select"] * {
            color: var(--text-primary) !important;
        }

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: var(--bg-card) !important;
            border-radius: var(--radius-sm) !important;
            padding: 4px !important;
            border: 1px solid var(--border-card) !important;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-family: 'Inter', sans-serif !important;
            padding: 8px 20px !important;
            transition: all 0.25s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-primary) !important;
            background: rgba(255, 255, 255, 0.05) !important;
        }

        .stTabs [aria-selected="true"] {
            background: var(--accent-gradient) !important;
            color: white !important;
            font-weight: 600 !important;
        }

        .stTabs [data-baseweb="tab-highlight"] {
            display: none !important;
        }

        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
        }

        /* ── Buttons ── */
        .stButton > button {
            background: var(--accent-gradient) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-sm) !important;
            padding: 10px 28px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
            letter-spacing: 0.02em;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(108, 99, 255, 0.45) !important;
        }

        .stButton > button:active {
            transform: translateY(0px) !important;
        }

        /* ── Download Buttons ── */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #00d4aa, #00b894) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-sm) !important;
            padding: 10px 28px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3) !important;
        }

        .stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(0, 212, 170, 0.45) !important;
        }

        /* ── Alerts / Info / Success / Error ── */
        [data-testid="stAlert"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-card) !important;
            border-radius: var(--radius-sm) !important;
            color: var(--text-primary) !important;
            backdrop-filter: blur(10px);
        }

        /* ── Spinner ── */
        .stSpinner > div {
            border-top-color: var(--accent-1) !important;
        }

        /* ── Metrics ── */
        [data-testid="stMetric"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-card) !important;
            border-radius: var(--radius) !important;
            padding: 16px 20px !important;
        }

        [data-testid="stMetricValue"] {
            color: var(--text-primary) !important;
        }

        [data-testid="stMetricLabel"] {
            color: var(--text-secondary) !important;
        }

        /* ── Divider ── */
        hr {
            border-color: var(--border-card) !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(108, 99, 255, 0.3);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(108, 99, 255, 0.5);
        }

        /* ── Custom hero header ── */
        .hero-header {
            text-align: center;
            padding: 2rem 0 1.5rem 0;
        }
        .hero-header .icon {
            font-size: 3rem;
            margin-bottom: 0.5rem;
            display: block;
        }
        .hero-header h1 {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.3rem;
        }
        .hero-header p {
            color: var(--text-secondary);
            font-size: 1.05rem;
            font-weight: 400;
            max-width: 500px;
            margin: 0 auto;
        }

        /* ── Domain badge ── */
        .domain-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 99px;
            padding: 6px 16px;
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 500;
            margin-top: 8px;
        }
        .domain-badge .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            display: inline-block;
            animation: pulse-dot 2s ease infinite;
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        /* ── Section label ── */
        .section-label {
            color: var(--text-muted);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.5rem;
        }

        /* ── Footer ── */
        .footer {
            text-align: center;
            padding: 2rem 0 1rem 0;
            color: var(--text-muted);
            font-size: 0.8rem;
            border-top: 1px solid var(--border-card);
            margin-top: 3rem;
        }
        .footer a {
            color: var(--accent-1);
            text-decoration: none;
        }

        /* ── Radio buttons in sidebar ── */
        .stRadio > div {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .stRadio > div > label {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-card) !important;
            border-radius: var(--radius-sm) !important;
            padding: 10px 14px !important;
            transition: all 0.25s ease;
            cursor: pointer;
        }

        .stRadio > div > label:hover {
            background: var(--bg-card-hover) !important;
            border-color: rgba(108, 99, 255, 0.3) !important;
        }

        /* ── st.code ── */
        code {
            color: var(--accent-2) !important;
            background: rgba(0, 212, 170, 0.1) !important;
            border-radius: 4px;
            padding: 2px 6px;
        }

        /* ── Markdown text ── */
        .stMarkdown p, .stMarkdown li {
            color: var(--text-primary) !important;
        }

        .stMarkdown a {
            color: var(--accent-1) !important;
        }

        /* ── Caption ── */
        .stCaption, small {
            color: var(--text-muted) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# SCRAPING BACKEND — all original logic intact
# ─────────────────────────────────────────────


def establish_Connection(link):
    try:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html.parser")
        return soup
    except:
        return None


def save_to_file(text, fname):
    if text:
        if isinstance(text, list):
            data = "\n".join([str(t) for t in text])
        else:
            data = text
        st.download_button(
            label="⬇️  Download Text File",
            data=data,
            file_name=fname,
            key=f"download_button_{fname}",
        )
    else:
        st.warning("⚠️ Website has no data!")


def button_Print(text, statement):
    if text is not None:
        with st.expander(f"📄 {statement}", expanded=False):
            st.write(text)


def link_Check(link):
    link_lower = link.lower().split("?")[0].split("#")[0]

    if link_lower.endswith(".pdf"):
        st.info("📑 This is a PDF file.")
        return "pdf"
    elif any(
        link_lower.endswith(ext) for ext in [".jpeg", ".jpg", ".png", ".svg", ".webp"]
    ):
        st.info("🖼️ This is an image file.")
        return "img"
    else:
        return 1


# ── Function 1: Embedded Links ──
def embedded_links(link):
    try:
        if link_Check(link) == 1:
            soup = establish_Connection(link)
            if not soup:
                return []
            links = soup.find_all("a")

            if links:
                embed_link = set()
                for link_tag in links:
                    href = link_tag.get("href")
                    if href and not href.startswith("#"):
                        absolute_link = urljoin(link, href)
                        embed_link.add(absolute_link)

                if embed_link:
                    embed_link = list(embed_link)
                    if utility == "Embedded Links":
                        fname = f"{domain_name.capitalize()}_Embedded_links_Website.txt"
                        save_to_file(embed_link, fname)
                        button_Print(embed_link, "See Embedded Links")
                    else:
                        return embed_link
                else:
                    if utility == "Embedded Links":
                        st.warning("⚠️ Website has no embedded links!")
                    return []
            else:
                if utility == "Embedded Links":
                    st.warning("⚠️ Website has no embedded links!")
                return []
        else:
            if utility == "Embedded Links":
                st.warning("⚠️ Provided link is not a normal webpage link.")
            return []
    except Exception as e:
        st.error(f"❌ Error in embedded_links: {e}")
        return []


# ── Function 2: Main Website Text Data ──
def main_website_text_Data(link):
    global visited_links
    try:
        if link_Check(link) == 1:
            if link not in visited_links:
                soup = establish_Connection(link)
                web_text = soup.get_text()

                if web_text is not None:
                    if utility == "Main Website Text Data":
                        fname = domain_name.capitalize() + "_Main_Website_Data.txt"
                        save_to_file(web_text, fname)
                        button_Print(web_text, "See Scraped Data")
                    else:
                        return web_text
                elif utility == "Main Website Text Data":
                    st.warning("⚠️ Website has no data!")
                    return ""
                else:
                    return ""

                visited_links.append(link)
            else:
                return ""
    except:
        visited_links.append(link)
        if utility == "Main Website Text Data":
            st.warning("⚠️ Website does not have any text data!")
        return ""


# ── Function 3: Main + Embedded Text Data ──
def main_website_text_embedded_link_text_Data(link):
    global visited_links
    web_text = []
    try:
        if link_Check(link) == 1:
            if link not in visited_links:
                web_text += main_website_text_Data(link)
                link = embedded_links(link)

                if link is not None:
                    for l in link:
                        web_text.append(main_website_text_Data(l))

                if web_text is not None and web_text != [""]:
                    if (
                        utility
                        == "Main Website Text Data along with Embedded Links Text Data"
                    ):
                        fname = (
                            domain_name.capitalize()
                            + "_Main_Website_Text_Data_Embedded_Links_Text_Data.txt"
                        )
                        save_to_file(web_text, fname)
                        button_Print(web_text, "See Scraped Data")
                    else:
                        return web_text
                else:
                    st.warning("⚠️ Website has no data!")
                    return ""
            else:
                return ""
    except:
        visited_links.append(link)
        return ""


# ── Function 4: Complete Text Data ──
def complete_text_data(link):
    try:
        if link_Check(link) == 1:
            complete_text = []
            main_website_text_Data(link)
            visited_links.append(link)
            links = embedded_links(link)

            if links is not None:
                for l in links:
                    complete_text.append(main_website_text_embedded_link_text_Data(l))

            if complete_text is not None:
                if utility == "Complete Website Text Data":
                    fname = domain_name.capitalize() + "_Complete_Website_Text_Data.txt"
                    save_to_file(complete_text, fname)
                    button_Print(complete_text, "See Scraped Data")
                else:
                    return ""
            else:
                st.warning("⚠️ Website has no text data!")
                return ""
    except:
        st.error("❌ An error occurred or the website has no data!")
        return ""


# ── PDF Text Extraction ──
def extract_text_from_pdf(url):
    try:
        if url not in visited_links:
            absolute_url = urljoin(link, url)
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(absolute_url, headers=headers, timeout=10)
            response.raise_for_status()

            if (
                "application/pdf"
                not in response.headers.get("Content-Type", "").lower()
            ):
                st.warning(f"⚠️ URL does not point to a PDF: {absolute_url}")
                visited_links.append(url)
                return ""

            pdf_content = BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_content)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            visited_links.append(url)
            return text
    except Exception as e:
        st.error(f"❌ Error extracting text from PDF ({url}): {e}")
        visited_links.append(url)
        return ""


# ── Function 5: PDF Link Data ──
def PDF_link_data(link):
    try:
        pdf_Data = []
        link_type = link_Check(link)

        if link_type == "pdf":
            pdf_Data.append(extract_text_from_pdf(link))
            if pdf_Data is not None and pdf_Data != [""]:
                fname = domain_name.capitalize() + "_Link_PDF_Data.txt"
                save_to_file(pdf_Data, fname)
                button_Print(pdf_Data, "See Scraped Data")
            else:
                st.warning("⚠️ PDF file has no data or is unreadable.")
        elif link_type == "img":
            pass
        else:
            st.warning("⚠️ PDF is unreadable or link has no PDF file.")
    except:
        st.error("❌ PDF is unreadable or link has no PDF file.")


# ── Function 6: Main Website + Embedded PDF Data ──
def main_website_PDF_embedded_link_PDF_Data(link):
    global visited_links
    pdf_Data = []
    try:
        if link_Check(link) == 1:
            links = embedded_links(link)
            if links is not None:
                for l in links:
                    pdf_Data.append(extract_text_from_pdf(l))

        if pdf_Data is not None and pdf_Data != [""]:
            if utility == "Main Website PDF Data along with Embedded Links PDF Data":
                fname = (
                    domain_name.capitalize()
                    + "_Main_Website_PDF_Data_Embedded_Links_PDF_Data.txt"
                )
                save_to_file(pdf_Data, fname)
                button_Print(pdf_Data, "See Scraped Data")
            else:
                return pdf_Data
        else:
            if utility == "Main Website PDF Data along with Embedded Links PDF Data":
                st.warning("⚠️ PDF file has no data or is unreadable.")
            return ""
    except:
        st.error("❌ Website has no PDF files data.")


# ── Function 7: Complete PDF Data ──
def complete_PDF_data(link):
    try:
        complete_text = []
        if link_Check(link) == 1:
            links = embedded_links(link)
            if links is not None:
                for l in links:
                    complete_text.append(main_website_PDF_embedded_link_PDF_Data(l))

        if complete_text is not None and complete_text != [""]:
            if utility == "Complete Website PDF Data":
                fname = domain_name.capitalize() + "_Complete_Website_PDF_Data.txt"
                save_to_file(complete_text, fname)
                button_Print(complete_text, "See Scraped Data")
            else:
                return complete_text
        else:
            st.warning("⚠️ PDF file has no data or is unreadable.")
            return ""
    except:
        st.error("❌ An error occurred or the website has no data!")
        return ""


# ── Function 8: Complete Text + PDF Data ──
def complete_text_pdf_Data(link):
    try:
        complete_text = []
        if link_Check(link) == 1:
            complete_text.append(complete_text_data(link))
            complete_text.append(complete_PDF_data(link))

        if complete_text is not None:
            fname = domain_name.capitalize() + "_Complete_Website_Text_PDF_Data.txt"
            save_to_file(complete_text, fname)
            button_Print(complete_text, "See Scraped Data")
        else:
            st.warning("⚠️ Website has no text and PDF data!")
    except:
        st.error("❌ An error occurred or the website has no data!")


# ── PDF Download Helper ──
def download_PDF(link, name, zip_filename):
    try:
        response = requests.get(link)
        temp = name

        with open(temp, "wb") as f:
            f.write(response.content)

        if not os.path.exists(zip_filename):
            with zipfile.ZipFile(zip_filename, "w") as zip_file:
                pass

        current_zip_size = os.path.getsize(zip_filename)

        if current_zip_size + os.path.getsize(temp) <= MAX_ZIP_FILE_SIZE:
            with zipfile.ZipFile(zip_filename, "a") as zip_file:
                zip_file.write(temp, arcname=name)
            st.success(f"✅ Added `{name}` to archive")
        else:
            st.warning("⚠️ Download limit reached — ZIP file is too large.")

        os.remove(temp)
    except Exception as e:
        st.error(f"❌ Failed to download PDF: {e}")


# ── PDF ZIP Download Button ──
def download_button_PDF():
    try:
        if os.path.exists(ZIP_PDF_FILENAME):
            with open(ZIP_PDF_FILENAME, "rb") as f:
                st.download_button(
                    "⬇️  Download PDF ZIP",
                    f,
                    file_name=f"{domain_name.capitalize()}_Zip_File_PDF.zip",
                    mime="application/zip",
                )
        else:
            st.info("📭 No PDF files available for download.")
    except Exception as e:
        st.error(f"❌ Error preparing ZIP: {e}")


# ── Function 9: Download PDF Files from Main Website ──
def main_download_PDF_Files(link):
    try:
        link_type = link_Check(link)

        if link_type == "pdf":
            name = link.split("/")[-1].replace(" ", "_")
            download_PDF(link, name, ZIP_PDF_FILENAME)
        elif link_type == "img":
            pass
        else:
            embed_links = embedded_links(link)
            if embed_links:
                for l in embed_links:
                    if l.lower().endswith(".pdf"):
                        name = l.split("/")[-1].replace(" ", "_")
                        download_PDF(l, name, ZIP_PDF_FILENAME)
    except Exception as e:
        st.error(f"❌ Error downloading PDFs: {e}")


# ── Function 10: Download All PDF Files (recursive) ──
def complete_download_PDF_Files(link):
    try:
        global visited_links
        link_type = link_Check(link)

        if link_type == "pdf" and link not in visited_links:
            if link.startswith("../../"):
                link = link.replace("../../", "https://")
            name = link.split("/")[-1].replace(" ", "_")
            link = link.replace(" ", "%20")
            download_PDF(link, name, ZIP_PDF_FILENAME)
            visited_links.append(link)
        elif link_type == "img":
            pass
        elif link not in visited_links and not link.endswith("pdf"):
            embed_links = embedded_links(link)
            if embed_links:
                for l in embed_links:
                    if l.endswith("pdf"):
                        if l.startswith("../../"):
                            l = l.replace("../../", "https://")
                        l = l.replace(" ", "%20")
                        name = l.split("/")[-1].replace(" ", "_")
                        download_PDF(l, name, ZIP_PDF_FILENAME)
                        visited_links.append(l)
                    else:
                        main_download_PDF_Files(l)
    except Exception as e:
        st.error(f"❌ Error downloading all PDFs: {e}")


# ── Image Download Helper ──
def download_Image(link, name):
    try:
        response = requests.get(link)
        with open(name, "wb") as f:
            f.write(response.content)

        if os.path.exists(ZIP_IMAGE_FILENAME):
            current_size = os.path.getsize(ZIP_IMAGE_FILENAME)
        else:
            current_size = 0

        if current_size + os.path.getsize(name) <= MAX_ZIP_FILE_SIZE:
            with zipfile.ZipFile(ZIP_IMAGE_FILENAME, "a") as zip_file:
                zip_file.write(name)
            os.remove(name)
        else:
            print(f"Zip file size limit exceeded ({MAX_ZIP_FILE_SIZE} bytes).")
    except Exception as e:
        print(f"Error downloading image: {e}")


# ── Image ZIP Download Button ──
def download_button_Image():
    try:
        with open("Zip_File_Image.zip", "rb") as f:
            st.download_button(
                "⬇️  Download Image ZIP",
                f,
                file_name=domain_name.capitalize() + "_Zip_File_Image.zip",
                mime="application/zip",
            )
    except:
        st.info("📭 Website has no image files.")


# ── Function 11: Download Images from Main Website ──
def main_download_Image_Files(link):
    try:
        link_type = link_Check(link)
        if link_type == "img":
            name = link.split("/")[-1].replace(" ", "_")
            link = link.replace(" ", "%20")
            download_Image(link, name)
        elif link_type == "pdf":
            pass
        else:
            soup = establish_Connection(link)
            if soup is not None:
                links = soup.find_all("img")
                embed_link = []

                if links is not None:
                    for link in links:
                        src = link.get("src")
                        if src is not None and not src.startswith("#"):
                            embed_link.append(src)

                    if embed_link is not None and embed_link != []:
                        for l in embed_link:
                            if (
                                l.endswith("jpeg")
                                or l.endswith("jpg")
                                or l.endswith("png")
                                or l.endswith("svg")
                                or l.endswith("webp")
                            ):
                                name = l.split("/")[-1].replace(" ", "_")
                                l = l.replace(" ", "%20")
                                download_Image(l, name)
    except:
        st.error("❌ An error occurred or website has no image files.")


# ── Function 12: Download All Images (recursive) ──
def complete_download_Image_Files(link):
    try:
        global visited_links
        link_type = link_Check(link)

        if link_type == "img" and link not in visited_links:
            name = link.split("/")[-1].replace(" ", "_")
            link = link.replace(" ", "%20")
            download_Image(link, name)
        elif link_type == "pdf":
            pass
        elif link not in visited_links and not link_type == "img":
            soup = establish_Connection(link)
            if soup is not None:
                links = soup.find_all("img")
                if links is not None:
                    embed_link = []
                    for link in links:
                        src = link.get("src")
                        if src is not None and not src.startswith("#"):
                            embed_link.append(src)

                if embed_link is not None and embed_link != [""]:
                    for l in embed_link:
                        if link_Check(l) == "img":
                            name = l.split("/")[-1].replace(" ", "_")
                            l = l.replace(" ", "%20")
                            download_Image(l, name)
                        else:
                            main_download_Image_Files(l)
        else:
            pass
    except:
        st.error("❌ An error occurred or website has no image files.")


# ── Utility: Remove temp files ──
def remove_files(fname):
    try:
        os.remove(fname)
    except:
        pass


# ── User Input ──
def user_input():
    global link, domain_name

    try:
        link = st.text_input(
            "🔗  WEBSITE URL",
            placeholder="https://example.com",
        )

        parsed_url = urlparse(link)
        domain_name = parsed_url.netloc.split(".")[0]
        if domain_name == "www":
            domain_name = parsed_url.netloc.split(".")[1]

        if link:
            st.markdown(
                f'<div class="domain-badge"><span class="dot"></span> Domain: <strong>{domain_name.capitalize()}</strong></div>',
                unsafe_allow_html=True,
            )

        return link, domain_name
    except Exception as e:
        st.error(f"❌ Please provide a valid URL — Error: {e}")


# ── Main execution logic ──
def main(utility):
    if not link:
        return

    with st.spinner("🔄 Scraping in progress… please wait"):
        if utility == "Embedded Links":
            embedded_links(link)
        elif utility == "Main Website Text Data":
            main_website_text_Data(link)
        elif utility == "Complete Website Text Data":
            complete_text_data(link)
        elif utility == "Main Website Text Data along with Embedded Links Text Data":
            main_website_text_embedded_link_text_Data(link)
        elif utility == "Extract Text from PDF Link":
            PDF_link_data(link)
        elif utility == "Main Website PDF Data along with Embedded Links PDF Data":
            main_website_PDF_embedded_link_PDF_Data(link)
        elif utility == "Complete Website PDF Data":
            complete_PDF_data(link)
        elif utility == "Complete Website Text and PDF Data":
            complete_text_pdf_Data(link)
        elif utility == "Download PDF Files From Main Website":
            main_download_PDF_Files(link)
            download_button_PDF()
            remove_files("Zip_File_PDF.zip")
        elif utility == "Download All PDF Files From Website":
            complete_download_PDF_Files(link)
            download_button_PDF()
            remove_files("Zip_File_PDF.zip")
        elif utility == "Download Image Files From Main Website":
            main_download_Image_Files(link)
            download_button_Image()
            remove_files("Zip_File_Image.zip")
        else:
            complete_download_Image_Files(link)
            download_button_Image()
            remove_files("Zip_File_Image.zip")


# ─────────────────────────────────────────────
# APP ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":

    # ── Page Config ──
    st.set_page_config(
        page_title="Web Scraper",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ── Inject dark theme CSS ──
    inject_custom_css()

    # ── Hero Header ──
    st.markdown(
        """
        <div class="hero-header">
            <span class="icon">🌐</span>
            <h1>Web Scraper</h1>
            <p>Extract text, PDFs, images & embedded links from any website in seconds.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Sidebar: Utility Selection ──
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
                <span style="font-size:2rem;">⚙️</span>
                <h3 style="margin:0.3rem 0 0 0; font-size:1.1rem;">Scraper Controls</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown('<div class="section-label">Category</div>', unsafe_allow_html=True)

        category = st.radio(
            "Select category",
            ["📝 Text Data", "📑 PDF Data", "⬇️ Download Files"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown('<div class="section-label">Utility</div>', unsafe_allow_html=True)

        if category == "📝 Text Data":
            utility = st.selectbox(
                "Utility",
                [
                    "Embedded Links",
                    "Main Website Text Data",
                    "Main Website Text Data along with Embedded Links Text Data",
                    "Complete Website Text Data",
                ],
                label_visibility="collapsed",
            )
        elif category == "📑 PDF Data":
            utility = st.selectbox(
                "Utility",
                [
                    "Extract Text from PDF Link",
                    "Main Website PDF Data along with Embedded Links PDF Data",
                    "Complete Website PDF Data",
                    "Complete Website Text and PDF Data",
                ],
                label_visibility="collapsed",
            )
        else:
            utility = st.selectbox(
                "Utility",
                [
                    "Download PDF Files From Main Website",
                    "Download All PDF Files From Website",
                    "Download Image Files From Main Website",
                    "Download All Image Files From Website",
                ],
                label_visibility="collapsed",
            )

        st.markdown("---")
        st.caption("💡 Select a category and utility, then enter a URL to start scraping.")

    # ── Main Content ──
    col_left, col_right = st.columns([2, 1])

    with col_left:
        user_input()

    with col_right:
        if link:
            st.markdown("")  # spacing
            st.markdown("")
            st.metric(label="Selected Utility", value=utility.split("along")[0].strip()[:30])

    st.markdown("---")

    # ── Results Area ──
    if link:
        st.markdown(
            f'<div class="section-label">Results — {utility}</div>',
            unsafe_allow_html=True,
        )
        main(utility)
    else:
        # Empty state
        st.markdown(
            """
            <div style="text-align:center; padding: 4rem 0; color: var(--text-muted);">
                <span style="font-size: 3rem; display:block; margin-bottom: 1rem; opacity:0.5;">🔍</span>
                <p style="font-size: 1.1rem; color: #6868a0;">Enter a website URL above to start scraping</p>
                <p style="font-size: 0.85rem; color: #4a4a78;">Choose a category from the sidebar, paste your URL, and let the magic happen.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Footer ──
    st.markdown(
        """
        <div class="footer">
            Built with ❤️ using <a href="https://streamlit.io" target="_blank">Streamlit</a> &amp; BeautifulSoup
        </div>
        """,
        unsafe_allow_html=True,
    )
