import './App.css'
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"
import StoryLoader from "./components/StoryLoader"
import StoryGenerator from "./components/StoryGenerator.jsx"

function App() {
  return (
    <Router>
      <div className="app-container">
        <header>
          <Link to="/" style={{ textDecoration: 'none' }}>
            <h1>Interactive Story Generator</h1>
          </Link>
        </header>
        <main>
          <div className="main-card">
            <Routes>
              <Route path="/story/:id" element={<StoryLoader />} />
              <Route path="/" element={<StoryGenerator />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  )
}

export default App