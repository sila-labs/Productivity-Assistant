import React, {useState} from "react";
import axios from "axios";
import "./styles.css"

const TaskPrioritzer = () => {
    // Component logic here
    const [task, setTasks] = useState("");
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post("http://127.0.0.1:5000/tasks/prioritize", {
                tasks: task.split("\n").map((task) => task.trim()),
            });
            setResponse(res.data.prioritized_tasks);
            setError(null);
        } catch (err) {
            setError("Error prioritizing tasks. Please try again.");
            setResponse(null);
        }
    };

    return (
        // JSX here -- the visual representation of the component
        <div className="container">
            <h1>Task Prioritizer</h1>
            <form onSubmit={handleSubmit}>
                <textarea
                    placeholder="Enter each task on a new line (e.g., 'Task 1\nTask 2\nTask 3')"
                    value={task}
                    onChange={(e) => setTasks(e.target.value)}
                    rows={5}
                    cols={40}
                />
                <br/>
                <button type="submit">Prioritize</button>
            </form>
            {response && (
                <div>
                     <h2>Prioritized Tasks</h2>
                     <pre>{response}</pre>
                </div>
            )}
            {error && <p style={{color: "red"}}>{error}</p>}
        </div>
    );
};

export default TaskPrioritzer;