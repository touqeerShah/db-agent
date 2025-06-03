import PropTypes from 'prop-types';
import { useState, useEffect, useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCopy } from '@fortawesome/free-solid-svg-icons';

import {
  faLink,
  faFileDownload,
  faDatabase,
  faSearch,
  faCheckCircle,
  faCode,
  faUserTie,
  faGlobe,
  faClipboard,
  faFlask,
  faPuzzlePiece,
  faHistory
} from '@fortawesome/free-solid-svg-icons';

const stepIcons = {
  detect_url: <FontAwesomeIcon icon={faLink} />, // Detecting URLs
  scrape_data: <FontAwesomeIcon icon={faFileDownload} />, // Scraping Data
  index: <FontAwesomeIcon icon={faDatabase} />, // Building Index
  process_query: <FontAwesomeIcon icon={faSearch} />, // Processing Query
  validate_code_existence: <FontAwesomeIcon icon={faCheckCircle} />, // Validating Code Existence
  transform_code_instruction: <FontAwesomeIcon icon={faCode} />, // Transforming Code Instruction
  supervisor: <FontAwesomeIcon icon={faUserTie} />, // Supervising Workflow
  general: <FontAwesomeIcon icon={faGlobe} />, // Handling General Queries
  summary: <FontAwesomeIcon icon={faClipboard} />, // Summarizing Data
  write_hardhat_test_case: <FontAwesomeIcon icon={faFlask} />, // Writing Hardhat Test Case
  write_foundry_test_case: <FontAwesomeIcon icon={faFlask} />, // Writing Foundry Test Case
  find_variability: <FontAwesomeIcon icon={faPuzzlePiece} />, // Finding Variability
  generate_chat_history: <FontAwesomeIcon icon={faHistory} />, // Generating Chat History
};
const humanReadableStep = {
  detect_url: "Detecting URLs",
  scrape_data: "Scraping Data",
  index: "Building Index",
  process_query: "Processing Query",
  validate_code_existence: "Validating Code Existence",
  transform_code_instruction: "Transforming Code Instruction",
  supervisor: "Supervising Workflow",
  general: "Handling General Queries",
  summary: "Summarizing Data",
  write_hardhat_test_case: "Writing Hardhat Test Case",
  write_foundry_test_case: "Writing Foundry Test Case",
  find_variability: "Finding Variability",
  generate_chat_history: "Generating Chat History",
  default: "Processing...",
};
const Messages = ({ messages, lastStep }) => {
  const messagesEndRef = useRef(null);


  // Auto-scroll to the bottom whenever messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className="chat-messages-chat">
      {messages.map((msg, index) => (
        <MessageBubble
          key={index}
          message={msg.message}
          type={msg.type}
          metadata={msg.metadata}
          lastStep={lastStep}
        />
      ))}
      {/* Empty div to scroll into view */}
      <div ref={messagesEndRef} />
    </div>
  );
};

Messages.propTypes = {
  messages: PropTypes.arrayOf(
    PropTypes.shape({
      message: PropTypes.string.isRequired,
      type: PropTypes.string.isRequired,
      metadata: PropTypes.object,
    })
  ).isRequired,
  lastStep: PropTypes.string.isRequired

};

const MessageBubble = ({ message, type, metadata, lastStep }) => {
  const [showMetadata, setShowMetadata] = useState(false);
  const [copySuccess, setCopySuccess] = useState('');

  // Toggle metadata visibility
  const toggleMetadata = () => setShowMetadata(!showMetadata);

  // Copy message to clipboard
  const copyToClipboard = () => {
    navigator.clipboard.writeText(message)
      .then(() => {
        setCopySuccess('Copied!');
        setTimeout(() => setCopySuccess(''), 1500); // Clear success message after 1.5s
      })
      .catch(() => setCopySuccess('Failed to copy'));
  };

  // Function to render message with formatted code blocks
  const renderMessageContent = () => {
    const codeBlockRegex = /```([^`]+)```/g;
    const linkRegex = /(https?:\/\/[^\s]+)/g;

    const parts = message.split(codeBlockRegex);

    return parts.map((part, index) => {
      if (index % 2 === 1) {
        // Code block
        return (
          <pre key={index} className="code-block">
            <code>{part}</code>
          </pre>
        );
      }

      // Process links in plain text
      const linkified = part.split(linkRegex).map((chunk, i) =>
        linkRegex.test(chunk) ? (
          <a key={i} href={chunk} target="_blank" rel="noopener noreferrer">
            {chunk}
          </a>
        ) : (
          chunk
        )
      );

      return <span key={index}>{linkified}</span>;
    });
  };

  return (
    <div className={`chat-message ${type === 'ai' ? 'chat-response' : 'chat-text-only'}`}>
      <div className="chat-message-content">
        <div className="chat-text">{renderMessageContent()}</div>

        {type === 'ai' && (
          <> <button className="copy-button" onClick={copyToClipboard}><FontAwesomeIcon icon={faCopy} /></button>
            {copySuccess && <span className="copy-success">{copySuccess}</span>}

            <button className="metadata-toggle" onClick={toggleMetadata}>
              {showMetadata ? '▲ Hide Details' : '▼ Show Details'}
            </button>
          </>
        )}
      </div>
      {type !== 'ai' && lastStep && <h6 className="chat-last-step">
        {stepIcons[lastStep]} {`${humanReadableStep[lastStep]} `} 
      </h6>}

      {showMetadata && type === 'ai' && (
        <div className="chat-metadata">
          <pre>{JSON.stringify(metadata, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

MessageBubble.propTypes = {
  message: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
  metadata: PropTypes.object,
  lastStep: PropTypes.string.isRequired
};


// export default MessageBubble;
export default Messages;
