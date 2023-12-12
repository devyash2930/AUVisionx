document.addEventListener("DOMContentLoaded", function() {
    // Fetch available and enrolled courses from the backend
    const availableCourses = [
        { id: "SE592", name: "Software Engineering 592" },
        { id: "SE593", name: "Software Engineering 593" },
        // Add more courses as needed
    ];

    const enrolledCourses = [
        { id: "SE592", name: "Software Engineering 592" },
        // Add more enrolled courses as needed
    ];

    const enrollContainer = document.getElementById("enroll-container");
    const enrolledContainer = document.getElementById("enrolled-container");

    // Display available courses
    displayCourses(enrollContainer, availableCourses, "Enroll", enrollCourse);

    // Display enrolled courses
    displayCourses(enrolledContainer, enrolledCourses, "Denroll", denrollCourse);
});

function displayCourses(container, courses, actionText, actionFunction) {
    courses.forEach(course => {
        const card = document.createElement("div");
        card.className = "course-card";
        card.innerHTML = `<p>${course.name} (${course.id})</p>`;

        const actionButton = document.createElement("button");
        actionButton.className = "enroll-button";
        actionButton.textContent = actionText;
        actionButton.addEventListener("click", () => actionFunction(course.id));

        card.appendChild(actionButton);
        container.appendChild(card);
    });
}

function enrollCourse(courseId) {
    // Send enrollment request to the backend
    console.log(`Enrolling in course: ${courseId}`);
}

function denrollCourse(courseId) {
    // Send denrollment request to the backend
    console.log(`Denrolling from course: ${courseId}`);
}
