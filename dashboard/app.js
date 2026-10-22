const navItems = document.querySelectorAll(".nav-item");
const pages = document.querySelectorAll(".page");

function showPage(pageId) {
    pages.forEach((page) => {
        page.classList.remove("active");
    });

    navItems.forEach((item) => {
        item.classList.remove("active");
    });

    const targetPage = document.getElementById(pageId);
    const targetNav = document.querySelector(`.nav-item[data-page="${pageId}"]`);

    if (targetPage) {
        targetPage.classList.add("active");
    }

    if (targetNav) {
        targetNav.classList.add("active");
    }
}

navItems.forEach((item) => {
    item.addEventListener("click", () => {
        const pageId = item.dataset.page;
        showPage(pageId);
    });
});

const newProjectButton = document.getElementById("new-project-button");
if (newProjectButton) {
    newProjectButton.addEventListener("click", () => {
        showPage("new-project");
    });
}

const viewLibraryButton = document.getElementById("view-library-button");
if (viewLibraryButton) {
    viewLibraryButton.addEventListener("click", () => {
        showPage("library");
    });
}


// ==========================================
// PINKCODES - LOCAL VIDEO PREVIEW
// ==========================================

(() => {
    const fileInput = document.getElementById("editor-video-input");
    const video = document.getElementById("editor-preview-video");
    const empty = document.getElementById("editor-preview-empty");
    const mediaCard = document.getElementById("editor-media-card");
    const fileName = document.getElementById("editor-file-name");
    const fileDetails = document.getElementById("editor-file-details");
    const seek = document.getElementById("editor-seek");
    const monitorTime = document.getElementById("editor-monitor-time");
    const timeEnd = document.getElementById("editor-time-end");
    const track = document.getElementById("editor-track-content");

    if (!fileInput || !video || !seek) return;

    let objectUrl = null;

    function formatTime(seconds) {
        if (!Number.isFinite(seconds) || seconds < 0) {
            return "00:00";
        }

        const total = Math.floor(seconds);
        const minutes = Math.floor(total / 60);
        const remaining = total % 60;

        return (
            String(minutes).padStart(2, "0") + ":" +
            String(remaining).padStart(2, "0")
        );
    }

    function updateTime() {
        const duration = video.duration;
        const current = video.currentTime;

        monitorTime.textContent =
            `${formatTime(current)} / ${formatTime(duration)}`;

        if (Number.isFinite(duration) && duration > 0) {
            seek.value = (current / duration) * 100;
        }
    }

    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];

        if (!file) return;

        video.pause();

        if (objectUrl) {
            URL.revokeObjectURL(objectUrl);
        }

        objectUrl = URL.createObjectURL(file);

        fileName.textContent = file.name;
        fileDetails.textContent =
            `${(file.size / 1024 / 1024).toFixed(1)} MB`;

        mediaCard.hidden = false;
        empty.hidden = true;
        video.hidden = false;

        seek.disabled = true;
        seek.value = 0;

        track.textContent = file.name;
        track.classList.add("has-video");

        monitorTime.textContent = "00:00 / 00:00";
        timeEnd.textContent = "00:00";

        video.src = objectUrl;
        video.load();
    });

    video.addEventListener("loadedmetadata", () => {
        const duration = video.duration;

        if (Number.isFinite(duration) && duration > 0) {
            timeEnd.textContent = formatTime(duration);
            seek.disabled = false;
        }

        updateTime();
    });

    video.addEventListener("timeupdate", updateTime);
    video.addEventListener("seeked", updateTime);

    video.addEventListener("error", () => {
        if (!video.src) return;

        fileDetails.textContent =
            "Nie mozna odtworzyc tego formatu w przegladarce.";
        seek.disabled = true;
    });

    seek.addEventListener("input", () => {
        const duration = video.duration;

        if (!Number.isFinite(duration) || duration <= 0) {
            return;
        }

        video.currentTime =
            (Number(seek.value) / 100) * duration;

        updateTime();
    });

    window.addEventListener("beforeunload", () => {
        if (objectUrl) {
            URL.revokeObjectURL(objectUrl);
        }
    });
})();
