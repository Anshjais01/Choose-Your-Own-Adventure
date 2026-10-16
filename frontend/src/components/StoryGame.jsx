import { useState, useEffect } from 'react'

function StoryGame({ story, onNewStory }) {
  const [currentNodeId, setCurrentNodeId] = useState(null)
  const [currentNode, setCurrentNode] = useState(null)
  const [options, setOptions] = useState([])
  const [isEnding, setIsEnding] = useState(false)
  const [isWinningEnding, setIsWinningEnding] = useState(false)

  useEffect(() => {
    if (story && story.root_node) {
      setCurrentNodeId(story.root_node.id)
    }
  }, [story])

  useEffect(() => {
    if (currentNodeId && story && story.all_nodes) {
      const node = story.all_nodes[currentNodeId]
      setCurrentNode(node)
      setIsEnding(node.is_ending)
      setIsWinningEnding(node.is_winning_ending)

      if (!node.is_ending && node.options && node.options.length > 0) {
        setOptions(node.options)
      } else {
        setOptions([])
      }
    }
  }, [currentNodeId, story])

  const chooseOption = (nodeId) => {
    setCurrentNodeId(nodeId)
  }

  const restartStory = () => {
    if (story && story.root_node) {
      setCurrentNodeId(story.root_node.id)
    }
  }

  return (
    <div className="story-game">
      <header className="story-header">
        <h2>{story.title}</h2>
      </header>

      <div className="story-content">
        {currentNode && (
          <div className="story-node">
            <p>{currentNode.content}</p>

            {isEnding ? (
              <div className={`story-ending ${isWinningEnding ? 'winning' : 'losing'}`}>
                <h3>{isWinningEnding ? "You won!" : "Your adventure has ended."}</h3>
                <p>
                  {isWinningEnding
                    ? "Congratulations! You have reached a victorious ending."
                    : "Fate has decided your outcome. You can restart or embark on a new quest."}
                </p>
              </div>
            ) : (
              <div className="story-options">
                <h3>What will you do?</h3>
                <div className="options-list">
                  {options.map((option, index) => (
                    <button
                      key={index}
                      onClick={() => chooseOption(option.node_id)}
                      className="option-btn"
                    >
                      {option.text}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        <div className="story-controls">
          <button onClick={restartStory} className="reset-btn">
            Restart Story
          </button>
          {onNewStory && (
            <button onClick={onNewStory} className="new-story-btn">
              New Story
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default StoryGame