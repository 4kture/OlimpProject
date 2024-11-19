function showPopup(id) {
    document.getElementById(id).style.display = 'flex';
}

function hidePopup(id) {
    document.getElementById(id).style.display = 'none';
}

function showTasksLink() {
    document.getElementById('tasks-link').style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
    var flashMessages = document.querySelector('.flash-messages');
    if (flashMessages) {
        flashMessages.style.display = 'block';
        setTimeout(function() {
            flashMessages.style.display = 'none';
            }, 3000);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('task-form');
    const taskList = document.querySelector('.task-list');

    taskForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const taskName = document.getElementById('task_name').value;
        const taskDescription = document.getElementById('task_description').value;

        const taskItem = document.createElement('div');
        taskItem.classList.add('task-item');
        taskItem.innerHTML = `
            <h3>${taskName}</h3>
            <button class="view-details-btn" onclick="openTaskPopup('${taskName}', '${taskDescription}')">View Details</button>
        `;

        taskList.appendChild(taskItem);

        taskForm.reset();
    });
});

function openTaskPopup(taskName, taskDescription) {
    document.getElementById('popup-task-name').innerText = taskName;
    document.getElementById('popup-task-description').innerText = taskDescription;
    document.getElementById('task-popup').style.display = 'flex';
}

function closeTaskPopup() {
    document.getElementById('task-popup').style.display = 'none';
}