document.addEventListener("DOMContentLoaded", function() {
    // Fetch courses from the backend
    const courses = [
        { id: "SE592", name: "Software Engineering 592", capacity: 20 },
        { id: "SE593", name: "Software Engineering 593", capacity: 12 },
        // Add more courses as needed
    ];

    const coursesContainer = document.getElementById("courses-list");
    const addCourseForm = document.getElementById("add-course");

    // Display existing courses
    displayCourses(coursesContainer, courses);

    // Add event listener for adding a course
    addCourseForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const courseName = document.getElementById("course-name").value;
        const courseCapacity = document.getElementById("course-capacity").value;

        // Send request to add the course to the backend
        console.log(`Adding course: ${courseName}, Capacity: ${courseCapacity}`);
        // You can add the logic to send the data to the backend here
    });
});

function displayCourses(container, courses) {
    container.innerHTML = "";
    courses.forEach(course => {
        const courseItem = document.createElement("li");
        courseItem.className = "course-item";
        courseItem.innerHTML = `<p>${course.name} (${course.id}) - Capacity: ${course.capacity}</p>`;
        container.appendChild(courseItem);
    });
}
