"""FindBlur — Know before you post.

Streamlit application for image blur and sharpness detection.
All analysis logic lives in blur_detector.py.
"""

import io
import os
import streamlit as st
import numpy as np
import pandas as pd
import cv2
from PIL import Image

import blur_detector

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="FindBlur — Know before you post.",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — minimal, just enough to make things look polished
# ---------------------------------------------------------------------------

st.markdown("""
<style>
    /* Tighten the top padding */
    .block-container {
        padding-top: 2rem;
    }

    /* Verdict badges */
    .verdict-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1.4rem;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .verdict-sharp {
        background: rgba(34, 197, 94, 0.15);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    .verdict-borderline {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .verdict-blurry {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Metric cards */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .metric-card {
        flex: 1;
        min-width: 120px;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .metric-card .label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        opacity: 0.6;
        margin-bottom: 0.25rem;
    }
    .metric-card .value {
        font-size: 1.3rem;
        font-weight: 600;
    }

    /* Status dot */
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
        margin-right: 6px;
        vertical-align: middle;
    }

    /* Header styling */
    .app-header {
        margin-bottom: 1.5rem;
    }
    .app-header h1 {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0;
        line-height: 1.1;
    }
    .app-header .tagline {
        font-size: 0.95rem;
        opacity: 0.5;
        margin-top: 0.3rem;
    }

    /* Review buttons */
    .review-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.3rem 0.7rem;
        border-radius: 6px;
        font-size: 0.8rem;
        cursor: pointer;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Table verdict badges (smaller) */
    .verdict-sm {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .verdict-sm-sharp {
        background: rgba(34, 197, 94, 0.15);
        color: #22c55e;
    }
    .verdict-sm-borderline {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
    }
    .verdict-sm-blurry {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
    }

    /* How it works section */
    .how-it-works {
        padding: 1rem 1.2rem;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* Review summary */
    .review-summary {
        display: flex;
        gap: 1.2rem;
        font-size: 0.85rem;
        padding: 0.6rem 0;
        flex-wrap: wrap;
    }
    .review-summary .item {
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    div[data-testid="stTabs"] button[data-baseweb="tab"] {
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------

def init_session_state():
    """Set up session state defaults on first run."""
    defaults = {
        "batch_results": [],
        "review_statuses": {},
        "threshold": 100.0,
        "sensitivity": "Balanced",
        "show_heatmap": True,
        "show_edge_map": True,
        "laplacian_weight": blur_detector.DEFAULT_LAPLACIAN_WEIGHT,
        "fft_weight": blur_detector.DEFAULT_FFT_WEIGHT,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session_state()


# ---------------------------------------------------------------------------
# UI helper functions
# ---------------------------------------------------------------------------

def render_header():
    """Compact app header."""
    st.markdown("""
    <div class="app-header">
        <h1>FIND<span style="font-weight:300;">BLUR</span></h1>
        <div class="tagline">Know before you post.</div>
        <div style="margin-top:0.5rem; font-size:0.8rem;">
            <span class="status-dot"></span>Detector ready
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_verdict_badge(verdict: str, message: str, large: bool = True):
    """Display a colored verdict badge."""
    icons = {"sharp": "✓", "borderline": "⚠", "blurry": "✕"}
    labels = {"sharp": "Sharp", "borderline": "Borderline", "blurry": "Blurry"}
    icon = icons.get(verdict, "?")
    label = labels.get(verdict, verdict)
    css_class = f"verdict-{verdict}"

    if large:
        st.markdown(
            f'<div class="verdict-badge {css_class}" style="font-size:1.4rem; padding:0.8rem 2rem;">'
            f'{icon} {label}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"<p style='opacity:0.7; margin-top:0.5rem;'>{message}</p>", unsafe_allow_html=True)
    else:
        st.markdown(
            f'<span class="verdict-sm verdict-sm-{verdict}">{icon} {label}</span>',
            unsafe_allow_html=True,
        )


def render_metric_cards(result: dict):
    """Display analysis metrics in a clean card row."""
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="label">Laplacian</div>
            <div class="value">{result['laplacian_score']}</div>
        </div>
        <div class="metric-card">
            <div class="label">FFT Energy</div>
            <div class="value">{result['fft_score']}</div>
        </div>
        <div class="metric-card">
            <div class="label">Combined Score</div>
            <div class="value">{result['combined_score']}</div>
        </div>
        <div class="metric-card">
            <div class="label">Confidence</div>
            <div class="value">{result['confidence']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_detection_breakdown(result: dict):
    """Show the normalized confidence breakdown."""
    with st.expander("Detection breakdown"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Laplacian confidence", f"{result['laplacian_confidence']}%")
            st.caption(f"Raw score: {result['laplacian_score']}")
        with col2:
            st.metric("FFT confidence", f"{result['fft_confidence']}%")
            st.caption(f"Raw score: {result['fft_score']}")

        st.progress(min(result["confidence"] / 100.0, 1.0), text=f"Combined: {result['combined_score']}%")


def render_image_comparison(original_rgb: np.ndarray, show_heatmap: bool, show_edge: bool):
    """Show original alongside diagnostic visualizations."""
    cols_needed = 1 + int(show_heatmap) + int(show_edge)
    cols = st.columns(cols_needed)

    idx = 0
    with cols[idx]:
        st.image(original_rgb, caption="Original", use_container_width=True)
    idx += 1

    if show_heatmap:
        heatmap = blur_detector.generate_laplacian_heatmap(
            cv2.cvtColor(original_rgb, cv2.COLOR_RGB2BGR)
        )
        with cols[idx]:
            st.image(heatmap, caption="Detail map", use_container_width=True)
        idx += 1

    if show_edge:
        edge_map = blur_detector.generate_edge_map(
            cv2.cvtColor(original_rgb, cv2.COLOR_RGB2BGR)
        )
        with cols[idx]:
            st.image(edge_map, caption="Edge map", use_container_width=True, clamp=True)


def render_review_controls(image_key: str):
    """Render manual review buttons for a single result."""
    current = st.session_state.review_statuses.get(image_key, "Not reviewed")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✓ Correct", key=f"correct_{image_key}",
                      type="primary" if current == "Correct" else "secondary"):
            st.session_state.review_statuses[image_key] = "Correct"
            st.rerun()
    with col2:
        if st.button("! Disagree", key=f"disagree_{image_key}",
                      type="primary" if current == "Disagree" else "secondary"):
            st.session_state.review_statuses[image_key] = "Disagree"
            st.rerun()
    with col3:
        status_display = current
        if current == "Correct":
            st.success(f"✓ {status_display}")
        elif current == "Disagree":
            st.warning(f"! {status_display}")
        else:
            st.caption(f"○ {status_display}")


def render_how_it_works():
    """Expandable explanation section."""
    with st.expander("How this works"):
        st.markdown("""
<div class="how-it-works">

FindBlur looks at tiny changes in brightness around edges.

Sharp photos usually contain more fine detail, which produces a stronger Laplacian response.

We also check high-frequency detail using FFT. Both signals are combined before deciding whether
an image looks sharp, borderline, or blurry.

The combined score is compared against your configured threshold. Images near the threshold
are marked as borderline so you can review them manually.

</div>
        """, unsafe_allow_html=True)


def render_review_summary():
    """Show counts of review statuses."""
    statuses = st.session_state.review_statuses
    correct = sum(1 for v in statuses.values() if v == "Correct")
    disagree = sum(1 for v in statuses.values() if v == "Disagree")
    total_results = len(st.session_state.batch_results)
    pending = total_results - correct - disagree

    st.markdown(f"""
    <div class="review-summary">
        <div class="item"><span style="color:#22c55e;">✓</span> Correct: {correct}</div>
        <div class="item"><span style="color:#f59e0b;">!</span> Disagree: {disagree}</div>
        <div class="item"><span style="opacity:0.5;">○</span> Pending: {pending}</div>
    </div>
    """, unsafe_allow_html=True)


def load_image(uploaded_file) -> tuple[np.ndarray | None, np.ndarray | None]:
    """Load an uploaded file into OpenCV (BGR) and RGB arrays.

    Returns (bgr_image, rgb_image) or (None, None) on failure.
    """
    try:
        file_bytes = uploaded_file.read()
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        nparr = np.frombuffer(file_bytes, np.uint8)
        bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if bgr is None:
            return None, None
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return bgr, rgb
    except Exception:
        return None, None


def get_current_settings() -> dict:
    """Read current analysis settings from session state."""
    return {
        "threshold": st.session_state.threshold,
        "sensitivity": st.session_state.sensitivity,
        "laplacian_weight": st.session_state.laplacian_weight,
        "fft_weight": st.session_state.fft_weight,
    }


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_sidebar():
    """Build the settings sidebar."""
    with st.sidebar:
        st.markdown("### FINDBLUR")
        st.markdown("---")

        # --- Detection ---
        st.markdown("**Detection**")

        st.session_state.sensitivity = st.selectbox(
            "Sensitivity",
            options=["Strict", "Balanced", "Lenient"],
            index=["Strict", "Balanced", "Lenient"].index(st.session_state.sensitivity),
            key="sensitivity_select",
        )

        preset = blur_detector.SENSITIVITY_PRESETS[st.session_state.sensitivity]
        st.caption(preset["description"])

        st.session_state.threshold = st.slider(
            "Laplacian threshold",
            min_value=0,
            max_value=1000,
            value=int(st.session_state.threshold),
            step=5,
            key="threshold_slider",
        )

        settings = blur_detector.get_effective_settings(
            st.session_state.threshold, st.session_state.sensitivity
        )
        st.markdown(f"**Effective threshold:** {settings['effective_threshold']:.0f}")
        st.markdown(f"**Borderline margin:** ±{settings['margin']}")

        st.markdown("---")

        # --- Analysis ---
        st.markdown("**Analysis**")

        lap_pct = st.slider(
            "Laplacian weight",
            min_value=0,
            max_value=100,
            value=int(st.session_state.laplacian_weight * 100),
            step=5,
            key="lap_weight_slider",
            format="%d%%",
        )
        st.session_state.laplacian_weight = lap_pct / 100.0
        st.session_state.fft_weight = 1.0 - st.session_state.laplacian_weight

        st.markdown(f"FFT weight: **{int(st.session_state.fft_weight * 100)}%**")

        st.markdown("---")

        # --- Display ---
        st.markdown("**Display**")

        st.session_state.show_heatmap = st.checkbox(
            "Show heatmap", value=st.session_state.show_heatmap, key="show_heatmap_cb"
        )
        st.session_state.show_edge_map = st.checkbox(
            "Show edge map", value=st.session_state.show_edge_map, key="show_edge_cb"
        )


render_sidebar()


# ---------------------------------------------------------------------------
# Main content — Tabs
# ---------------------------------------------------------------------------

render_header()

tab_single, tab_batch, tab_camera, tab_about = st.tabs([
    "Single Check", "Batch Check", "Live Camera", "Settings / About"
])


# ---------------------------------------------------------------------------
# Tab 1: Single Check
# ---------------------------------------------------------------------------

with tab_single:
    uploaded = st.file_uploader(
        "Drop an image here",
        type=["jpg", "jpeg", "png", "webp"],
        key="single_upload",
        help="JPG · PNG · WEBP",
    )

    if uploaded is not None:
        bgr, rgb = load_image(uploaded)

        if bgr is None:
            st.error("Couldn't read this image. Try uploading a JPG, PNG, or WEBP file.")
        else:
            # Analyze
            settings = get_current_settings()
            result = blur_detector.analyze_image(
                bgr,
                threshold=settings["threshold"],
                sensitivity=settings["sensitivity"],
                laplacian_weight=settings["laplacian_weight"],
                fft_weight=settings["fft_weight"],
            )

            # Image comparison
            render_image_comparison(
                rgb,
                st.session_state.show_heatmap,
                st.session_state.show_edge_map,
            )

            st.markdown("")

            # Verdict
            render_verdict_badge(result["verdict"], result["message"], large=True)

            st.markdown("")

            # Metrics
            render_metric_cards(result)

            # Breakdown
            render_detection_breakdown(result)

            st.markdown("")

            # Review
            st.markdown("**Review**")
            render_review_controls(uploaded.name)

            st.markdown("---")

            # How it works
            render_how_it_works()
    else:
        st.markdown("")
        st.markdown(
            "<p style='text-align:center; opacity:0.4; padding:3rem 0;'>"
            "JPG · PNG · WEBP</p>",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Tab 2: Batch Check
# ---------------------------------------------------------------------------

with tab_batch:
    batch_files = st.file_uploader(
        "Upload images",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        key="batch_upload",
        help="Select multiple files.",
    )

    if batch_files:
        # Only re-analyze if files changed
        current_names = sorted([f.name for f in batch_files])
        prev_names = sorted([r["filename"] for r in st.session_state.batch_results]) if st.session_state.batch_results else []

        if current_names != prev_names:
            settings = get_current_settings()
            results = []
            errors = []

            progress_bar = st.progress(0, text="Analyzing images...")
            total = len(batch_files)

            for i, f in enumerate(batch_files):
                bgr, rgb = load_image(f)
                if bgr is None:
                    errors.append(f.name)
                    continue

                result = blur_detector.analyze_image(
                    bgr,
                    threshold=settings["threshold"],
                    sensitivity=settings["sensitivity"],
                    laplacian_weight=settings["laplacian_weight"],
                    fft_weight=settings["fft_weight"],
                )
                result["filename"] = f.name

                # Create a small thumbnail for display
                thumb = cv2.resize(rgb, (60, 60), interpolation=cv2.INTER_AREA)
                result["thumbnail"] = thumb

                results.append(result)

                progress_bar.progress(
                    (i + 1) / total,
                    text=f"Analyzing images... {i + 1} / {total}",
                )

            progress_bar.empty()

            st.session_state.batch_results = results

            if errors:
                st.warning(
                    f"{len(errors)} file{'s' if len(errors) > 1 else ''} couldn't be processed. "
                    f"The remaining {len(results)} file{'s' if len(results) > 1 else ''} "
                    f"{'were' if len(results) > 1 else 'was'} analyzed successfully."
                )

        # --- Filtering & sorting controls ---
        results = st.session_state.batch_results

        if results:
            col_filter, col_sort, col_order = st.columns(3)

            with col_filter:
                filter_options = ["All", "Sharp", "Borderline", "Blurry", "Reviewed", "Disagree"]
                filter_choice = st.selectbox("Filter", filter_options, key="batch_filter")

            with col_sort:
                sort_options = ["Filename", "Laplacian", "FFT", "Combined Score", "Confidence", "Verdict"]
                sort_choice = st.selectbox("Sort by", sort_options, key="batch_sort")

            with col_order:
                order_choice = st.selectbox("Order", ["Highest first", "Lowest first"], key="batch_order")

            # Apply filter
            filtered = results.copy()
            if filter_choice == "Sharp":
                filtered = [r for r in filtered if r["verdict"] == "sharp"]
            elif filter_choice == "Borderline":
                filtered = [r for r in filtered if r["verdict"] == "borderline"]
            elif filter_choice == "Blurry":
                filtered = [r for r in filtered if r["verdict"] == "blurry"]
            elif filter_choice == "Reviewed":
                filtered = [r for r in filtered if
                            st.session_state.review_statuses.get(r["filename"], "Not reviewed") != "Not reviewed"]
            elif filter_choice == "Disagree":
                filtered = [r for r in filtered if
                            st.session_state.review_statuses.get(r["filename"]) == "Disagree"]

            # Apply sort
            sort_keys = {
                "Filename": lambda r: r["filename"].lower(),
                "Laplacian": lambda r: r["laplacian_score"],
                "FFT": lambda r: r["fft_score"],
                "Combined Score": lambda r: r["combined_score"],
                "Confidence": lambda r: r["confidence"],
                "Verdict": lambda r: {"sharp": 0, "borderline": 1, "blurry": 2}.get(r["verdict"], 3),
            }
            reverse = order_choice == "Highest first"
            if sort_choice == "Filename":
                reverse = not reverse  # A-Z vs Z-A
            filtered.sort(key=sort_keys.get(sort_choice, lambda r: r["combined_score"]), reverse=reverse)

            # Review summary
            render_review_summary()

            st.markdown("---")

            # Results table
            if not filtered:
                st.info("No images match the current filter.")
            else:
                for r in filtered:
                    with st.container():
                        c_thumb, c_name, c_lap, c_fft, c_combined, c_verdict, c_review = st.columns(
                            [0.8, 2, 1, 1, 1, 1.2, 1.5]
                        )

                        with c_thumb:
                            st.image(r["thumbnail"], width=50)

                        with c_name:
                            st.markdown(f"**{r['filename']}**")

                        with c_lap:
                            st.caption("Laplacian")
                            st.markdown(f"**{r['laplacian_score']}**")

                        with c_fft:
                            st.caption("FFT")
                            st.markdown(f"**{r['fft_score']}**")

                        with c_combined:
                            st.caption("Combined")
                            st.markdown(f"**{r['combined_score']}**")

                        with c_verdict:
                            st.caption("Verdict")
                            render_verdict_badge(r["verdict"], "", large=False)

                        with c_review:
                            status = st.session_state.review_statuses.get(r["filename"], "Not reviewed")
                            review_val = st.selectbox(
                                "Review",
                                options=["Not reviewed", "Correct", "Disagree"],
                                index=["Not reviewed", "Correct", "Disagree"].index(status),
                                key=f"review_{r['filename']}",
                                label_visibility="collapsed",
                            )
                            if review_val != status:
                                st.session_state.review_statuses[r["filename"]] = review_val
                                st.rerun()

                    st.markdown(
                        "<hr style='margin:0.3rem 0; border:none; border-top:1px solid rgba(255,255,255,0.06);'>",
                        unsafe_allow_html=True,
                    )

            # CSV export
            st.markdown("")
            csv_data = []
            for r in results:
                csv_data.append({
                    "filename": r["filename"],
                    "laplacian_score": r["laplacian_score"],
                    "fft_score": r["fft_score"],
                    "combined_score": r["combined_score"],
                    "confidence": r["confidence"],
                    "verdict": r["verdict"],
                    "review_status": st.session_state.review_statuses.get(r["filename"], "Not reviewed"),
                })

            csv_df = pd.DataFrame(csv_data)
            csv_buffer = csv_df.to_csv(index=False)

            st.download_button(
                "Download CSV",
                data=csv_buffer,
                file_name="findblur_results.csv",
                mime="text/csv",
                key="csv_download",
            )
    else:
        st.markdown(
            "<p style='text-align:center; opacity:0.4; padding:3rem 0;'>"
            "Upload multiple images to analyze them as a batch.</p>",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Tab 3: Live Camera
# ---------------------------------------------------------------------------

with tab_camera:
    st.markdown("**Camera Check**")
    st.caption("Capture a photo and check its sharpness.")

    camera_image = st.camera_input("Capture", key="camera_capture", label_visibility="collapsed")

    if camera_image is not None:
        bgr, rgb = load_image(camera_image)

        if bgr is None:
            st.error("Couldn't process the captured image. Please try again.")
        else:
            settings = get_current_settings()
            result = blur_detector.analyze_image(
                bgr,
                threshold=settings["threshold"],
                sensitivity=settings["sensitivity"],
                laplacian_weight=settings["laplacian_weight"],
                fft_weight=settings["fft_weight"],
            )

            # Show captured image with visualizations
            render_image_comparison(
                rgb,
                st.session_state.show_heatmap,
                st.session_state.show_edge_map,
            )

            st.markdown("")

            # Verdict
            render_verdict_badge(result["verdict"], result["message"], large=True)

            st.markdown("")

            # Metrics
            render_metric_cards(result)

            # Breakdown
            render_detection_breakdown(result)

            st.markdown("")
            st.caption("Capture another image above to analyze again.")


# ---------------------------------------------------------------------------
# Tab 4: Settings / About
# ---------------------------------------------------------------------------

with tab_about:
    st.markdown("### Detection Settings")

    settings = blur_detector.get_effective_settings(
        st.session_state.threshold, st.session_state.sensitivity
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sensitivity", st.session_state.sensitivity)
        st.metric("Base threshold", int(st.session_state.threshold))
    with col2:
        st.metric("Effective threshold", f"{settings['effective_threshold']:.0f}")
        st.metric("Borderline margin", f"±{settings['margin']}")
    with col3:
        st.metric("Laplacian weight", f"{int(st.session_state.laplacian_weight * 100)}%")
        st.metric("FFT weight", f"{int(st.session_state.fft_weight * 100)}%")

    st.markdown("---")

    st.markdown("### About FindBlur")

    st.markdown("""
FindBlur checks image detail before you publish.

It combines edge-detail analysis with frequency analysis
to give you a second opinion on image sharpness.

All processing happens locally in your browser session.
No images are uploaded to any external server.
    """)

    st.markdown("---")

    with st.expander("Setup"):
        st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")
        st.caption("Requires Python 3.11+")

    st.markdown("---")

    # How it works
    render_how_it_works()
