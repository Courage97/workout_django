document.addEventListener('DOMContentLoaded', function () {
    const exerciseContainer = document.getElementById('exerciseContainer');
    const addExerciseBtn = document.getElementById('addExercise');
    const presetCards = document.querySelectorAll('.preset-card');
    const presetTypeInput = document.getElementById('presetType');
    const clearWorkoutBtn = document.getElementById('clearWorkout');

    const presets = {
        beginner: [
            { name: 'Walking', target: 30, unit: 'minutes' },
            { name: 'Push-ups', target: 10, unit: 'count' },
            { name: 'Squats', target: 15, unit: 'count' },
            { name: 'Plank', target: 1, unit: 'minutes' },
            { name: 'Stretching', target: 10, unit: 'minutes' },
        ],
        'weight-loss': [
            { name: 'Running', target: 30, unit: 'minutes' },
            { name: 'Jumping Jacks', target: 50, unit: 'count' },
            { name: 'Burpees', target: 20, unit: 'count' },
            { name: 'Mountain Climbers', target: 30, unit: 'count' },
            { name: 'High Knees', target: 2, unit: 'minutes' },
        ],
        muscle: [
            { name: 'Bench Press', target: 12, unit: 'count' },
            { name: 'Deadlifts', target: 10, unit: 'count' },
            { name: 'Pull-ups', target: 8, unit: 'count' },
            { name: 'Shoulder Press', target: 12, unit: 'count' },
            { name: 'Squats', target: 15, unit: 'count' },
        ],
    };

    // Initialize: Check for saved exercises or enable preset cards
    initializeWorkout();

    // Event Listener: Add a new exercise entry
    addExerciseBtn.addEventListener('click', addExerciseEntry);

    // Event Listener: Clear workout plan
    if (clearWorkoutBtn) {
        clearWorkoutBtn.addEventListener('click', clearWorkoutPlan);
    }

    // Preset card selection
    presetCards.forEach(card => {
        card.addEventListener('click', () => {
            if (!card.classList.contains('disabled')) {
                presetCards.forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                presetTypeInput.value = card.dataset.preset;
                loadPresetExercises(card.dataset.preset);
            }
        });
    });

    // Function: Add a new exercise entry
    function addExerciseEntry(name = '', target = '', unit = 'minutes') {
        const exerciseDiv = document.createElement('div');
        exerciseDiv.className = 'exercise-entry';
        exerciseDiv.innerHTML = `
            <input type="text" name="exercise_name[]" placeholder="Exercise name" value="${name}" required>
            <input type="number" name="exercise_target[]" placeholder="Target" value="${target}" required min="1">
            <select name="exercise_unit[]">
                <option value="minutes" ${unit === 'minutes' ? 'selected' : ''}>Minutes</option>
                <option value="count" ${unit === 'count' ? 'selected' : ''}>Count</option>
            </select>
            <button type="button" class="remove-btn" onclick="this.parentElement.remove()">×</button>
        `;
        exerciseContainer.appendChild(exerciseDiv);
    }

    // Function: Load preset exercises
    function loadPresetExercises(preset) {
        exerciseContainer.innerHTML = '';
        presets[preset].forEach(exercise => {
            addExerciseEntry(exercise.name, exercise.target, exercise.unit);
        });
    }

    // Function: Clear workout plan
    function clearWorkoutPlan() {
        if (confirm('Are you sure you want to clear your current workout plan?')) {
            exerciseContainer.innerHTML = ''; // Clear exercises
            presetCards.forEach(card => card.classList.remove('disabled', 'selected')); // Enable presets
            presetTypeInput.value = ''; // Reset preset type
        }
    }

    // Function: Initialize workout
    function initializeWorkout() {
        if (exerciseContainer.children.length > 0) {
            // Disable preset cards if exercises exist
            presetCards.forEach(card => card.classList.add('disabled'));
        }
    }
});


// dashboard js


