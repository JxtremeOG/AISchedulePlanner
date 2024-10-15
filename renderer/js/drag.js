function attachDragEvents() {
    const draggables = document.querySelectorAll(".course-card");
    const droppables = document.querySelectorAll(".term-div");

    draggables.forEach((course) => {
        course.addEventListener("dragstart", () => {
            course.classList.add("is-dragging");
        });

        course.addEventListener("dragend", () => {
            course.classList.remove("is-dragging");
        });
    });

    droppables.forEach((zone) => {
        zone.addEventListener("dragover", (e) => {
            e.preventDefault();

            const coursesContainer = zone.querySelector(".courses-container");
            const draggedItem = document.querySelector(".is-dragging");

            if (!draggedItem) {
                console.log("No item is being dragged");
                return;
            }

            const closestCourse = insertLeftCourse(coursesContainer, e.clientX);
            if (!closestCourse) {
                coursesContainer.appendChild(draggedItem);
            } else {
                coursesContainer.insertBefore(draggedItem, closestCourse);
            }
        });
    });
}

const insertLeftCourse = (zone, mouseX) => {
    const els = zone.querySelectorAll(".course-card:not(.is-dragging)");
    let closestCourse = null;
    let closestOffset = Number.NEGATIVE_INFINITY;

    els.forEach((course) => {
        const { left } = course.getBoundingClientRect();
        const offset = mouseX - left;

        if (offset < 0 && offset > closestOffset) {
            closestOffset = offset;
            closestCourse = course;
        }
    });

    return closestCourse;
};
