import PropTypes from 'prop-types';
import { useState, useEffect, useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCopy } from '@fortawesome/free-solid-svg-icons';
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import {
  faLink,
  faDatabase,
  faSearch,
  faCheckCircle,
  
} from '@fortawesome/free-solid-svg-icons';

const stepIcons = {
  classify_user_intent: <FontAwesomeIcon icon={faLink} />, // Detecting URLs
  query_database: <FontAwesomeIcon icon={faDatabase} />, // Scraping Data
  respond_general: <FontAwesomeIcon icon={faSearch} />, // Processing Query
  stream: <FontAwesomeIcon icon={faCheckCircle} />, // Validating Code Existence
  summary: <FontAwesomeIcon icon={faCheckCircle} />, // Validating Code Existence
};
const humanReadableStep = {
  classify_user_intent: "Classify User Intent",
  query_database: "Query Database",
  respond_general: "Respond General",
  summary: "Summary",
  stream: "Stream",
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
  if (!message || typeof message !== 'string') return null;
  console.log("message : ",message)
  // If message starts with a Markdown code block like ```markdown ... ```
  const markdownCodeBlockMatch = message.match(/```(?:markdown)?\s*([\s\S]*?)```/);
  console.log("markdownCodeBlockMatch",markdownCodeBlockMatch)
  if (message) {
    // Extract and render the inner Markdown content
    // const markdownContent = markdownCodeBlockMatch[1];

    return (
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
        components={{
          code({ node, inline, className, children, ...props }) {
            return !inline ? (
              <pre className="bg-gray-800 text-white p-2 rounded-md overflow-x-auto">
                <code className={className} {...props}>{"= = "+children}</code>
              </pre>
            ) : (
              <code className="bg-gray-200 px-1 rounded"> {children}</code>
            );
          },
          a({ href, children }) {
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 underline"
              >
                {children}
              </a>
            );
          },
        }}
      >
        {message}
      </ReactMarkdown>
    );
  }

  // Fallback: just render message as normal text with links auto-detected
  const linkRegex = /(https?:\/\/[^\s]+)/g;
  const parts = message.split(linkRegex);

  return (
    <span>
      {parts.map((chunk, index) =>
        linkRegex.test(chunk) ? (
          <a key={index} href={chunk} target="_blank" rel="noopener noreferrer">
            {chunk}
          </a>
        ) : (
          <span key={index}>{chunk}</span>
        )
      )}
    </span>
  );
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
