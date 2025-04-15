// Modal
var modal = document.getElementById("myModal");
var modalContent = document.getElementById("modal-content");
function refreshOnclickModal() {
    const media = document.getElementsByClassName('media-element');
    for (var m of media) {
        if (m.tagName === "IMG") {
            m.onclick = function () {
                modal.style.display = "block";
                const content_element = document.createElement('img');
                content_element.src = this.src;
                modalContent.appendChild(content_element);
            }
        }
    }
}
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modalContent.innerHTML = '';
        modal.style.display = 'none';
    }
});

// Lazy Loading
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const media = entry.target;
            if (media.tagName == 'IMG') {
                media.src = media.dataset.src;
                media.classList.remove('lazy-load');
                observer.unobserve(media);
            } else if (media.tagName == 'VIDEO') {
                for (var source in media.children) {
                    var videoSource = media.children[source];
                    if (typeof videoSource.tagName === "string" && videoSource.tagName === "SOURCE") {
                        videoSource.src = videoSource.dataset.src;
                    }
                }
                media.load();
                media.load();
                media.classList.remove('lazy-load');
                observer.unobserve(media);
            }
        }
    });
});
function refreshLazyLoading() {
    document.querySelectorAll('.lazy-load').forEach(media => {
        observer.observe(media);
    });
}

// building the gallery
function buildGallery(media_by_year, videos) {
    gallery = document.getElementById('gallery');
    gallery.innerHTML = '';
    for (const [year, files] of Object.entries(media_by_year)) {

        var gallery_year = document.createElement('div');
        gallery_year.classList.add("gallery");

        // create header
        const hr = document.createElement('hr');
        hr.classList.add("my-2");
        const header = document.createElement('h1');
        header.classList.add("my-2");
        header.textContent = year;
        gallery.appendChild(hr);
        gallery.appendChild(header);

        for (var f of files) {
            f = 'media/' + year + '/' + f;
            if (f.endsWith('.jpg')) {
                // create img
                const image = document.createElement('img');
                image.classList.add("media-element", "lazy-load");
                image.dataset.src = 'static/' + f;

                // append to parent
                gallery_year.appendChild(image);

            } else if (videos) {
                //create video
                const video = document.createElement('video');
                video.classList.add("media-element", "lazy-load");
                video.preload = 'none';
                video.controls = true;

                // create source
                const source = document.createElement('source');
                source.dataset.src = 'static/' + f;
                source.type = "video/mp4";

                // append to parent
                video.appendChild(source);
                gallery_year.appendChild(video);
            }
        }
        gallery.appendChild(gallery_year);
    }

    refreshOnclickModal();
    refreshLazyLoading();
}
