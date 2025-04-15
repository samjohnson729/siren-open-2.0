function updateLiveSummaryScrollableContentHeight() {
    const scrollableContent = document.getElementById('live-summary-content');
    const liveHoleSelectionHeight = document.getElementById('live-hole-selection').offsetHeight;
    const baseNavBarHeight = document.getElementById('base-navbar').offsetHeight
    scrollableContent.style.height = window.innerHeight - (liveHoleSelectionHeight + baseNavBarHeight) + 'px';
}

function updateLiveDetailScrollableContentHeight() {
    const scrollableContent = document.getElementById('live-detail-content');
    const liveHoleSelectionHeight = document.getElementById('live-hole-selection').offsetHeight;
    const baseNavBarHeight = document.getElementById('base-navbar').offsetHeight
    scrollableContent.style.height = window.innerHeight - (liveHoleSelectionHeight + baseNavBarHeight) + 'px';
}

function updateScrollableContentHeight() {

    try{
        updateLiveSummaryScrollableContentHeight();
    } catch {}
    
    try{
        updateLiveDetailScrollableContentHeight();
    } catch {}
    
}

window.addEventListener('resize', updateScrollableContentHeight);
window.addEventListener('DOMContentLoaded', updateScrollableContentHeight);

function saveScrollPositions() {
    live_hole_selection = document.getElementById("live-hole-selection");
    live_detail_content = document.getElementById("live-detail-content");

    localStorage.setItem('hole-scroll-bar-pos', live_hole_selection.scrollLeft);
    localStorage.setItem('live-detail-scroll-bar-pos', live_detail_content.scrollTop);
}

function loadScrollPositions() {
    live_hole_selection = document.getElementById("live-hole-selection");
    live_detail_content = document.getElementById("live-detail-content");

    var live_hole_selection_pos = localStorage.getItem('hole-scroll-bar-pos');
    var live_detail_content_pos = localStorage.getItem('live-detail-scroll-bar-pos');

    if (live_hole_selection_pos) live_hole_selection.scrollLeft = live_hole_selection_pos;
    if (live_detail_content_pos) live_detail_content.scrollTop = live_detail_content_pos;
}

window.addEventListener("beforeunload", saveScrollPositions);
window.addEventListener("load", loadScrollPositions);
