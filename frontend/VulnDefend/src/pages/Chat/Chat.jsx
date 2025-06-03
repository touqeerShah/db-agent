import './ChatPage.css';
import { useParams, useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useState, useEffect } from 'react';
import { faPaperPlane, faUpload, faSpinner } from '@fortawesome/free-solid-svg-icons';
import ChatNav from "../../components/Chat/Nav";
import ChatHistory from "../../components/Chat/ChatHistory";
import Messages from "../../components/Chat/Mesages";
import { defer, useLoaderData, Await } from "react-router-dom";
import { requireAuth } from "../../utils/auth";
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export async function loader({ request }) {
  const idToken = localStorage.getItem("loggedin");
  await requireAuth(request);

  try {
    const response = await fetch(`${BACKEND_URL}/api/list_chat/`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${idToken}`
      }
    });

    if (!response.ok) {
      throw new Error("Failed to fetch chat list.");
    }

    const chatList = await response.json();
    return defer({
      loginResponse: { isLogin: true, googleId: idToken },
      chatList: chatList,
    });
  } catch (error) {
    console.error("Error fetching chat list:", error);
    return defer({
      loginResponse: { isLogin: false, googleId: idToken },
      chatList: [],
    });
  }
}
async function generateHash(id) {
  const timestamp = Date.now().toString();
  const data = id + timestamp;
  const encoder = new TextEncoder();
  const dataUint8 = encoder.encode(data);
  const hashBuffer = await crypto.subtle.digest("SHA-256", dataUint8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));

  // Convert each byte to a two-character hex string and join them
  const hash = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

  // Ensure the hash is exactly 64 characters long (truncate or pad if necessary)
  return hash.length === 64 ? hash : hash.slice(0, 64);
}
const ChatPage = () => {
  const { id, chatid: initialChatid } = useParams();
  const dataPromise = useLoaderData();
  const navigate = useNavigate();

  const [chatid, setChatid] = useState(initialChatid || "");
  const [CHAT_URL, setChatUrl] = useState("");
  const [message, setMessage] = useState('');
  const [fileDetails, setFileDetails] = useState(null);
  const [lineCount, setLineCount] = useState(1);
  const [footerHeight, setFooterHeight] = useState(10);
  const [textArea, setTextArea] = useState(100);
  const [chatMessages, setChatMessages] = useState([]);
  const [firstMessageSent, setFirstMessageSent] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [chatList, setChatList] = useState(dataPromise.chatList);
  const [reloadChatList, setReloadChatList] = useState(false);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [lastStep, setLastStep] = useState("");

  const BASE_URL = `${BACKEND_URL}/api/report_stream`;

  // Reload chat list when first message is sent and response received
  useEffect(() => {
    if (reloadChatList) {
      fetchChatList();
      setReloadChatList(false);
    }
  }, [reloadChatList]);

  useEffect(() => {
    if (chatid) {
      setChatUrl(`${BASE_URL}/${chatid}/`);
      navigate(`/chat/${id}/${chatid}`);
      fetchChatMessages()
    }
  }, [chatid]);

  const fetchChatList = async () => {
    const idToken = localStorage.getItem("loggedin");

    try {
      const response = await fetch(`${BACKEND_URL}/api/list_chat/`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${idToken}`
        }
      });

      if (response.ok) {
        const updatedChatList = await response.json();
        setChatList(updatedChatList);
      } else if (response.status === 401) {
        // Token verification failed - clear token and redirect to login
        localStorage.removeItem("loggedin");
        navigate("/login?message=Your session has expired. Please log in again.");
      } else {
        console.error("Failed to reload chat list.");
      }
    } catch (error) {
      console.error("Error reloading chat list:", error);
      navigate("/login?message=An error occurred. Please log in again.");
    }
  };

  const fetchChatMessages = async () => {
    const idToken = localStorage.getItem("loggedin");

    try {
      setIsLoadingMessages(true);
      const response = await fetch(`${BACKEND_URL}/api/chat_details/${chatid}/`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${idToken}`,
          "Content-Type": "application/json",
        }
      });

      if (response.ok) {
        const messages = await response.json();

        // console.log("messages", messages)
        // Map the messages to the expected structure
        const formattedMessages = messages.flatMap(msg => {
          const formatted = [];

          if (msg.question) {
            // User message
            formatted.push({
              message: msg.question,
              type: 'user',
              metadata: {
                created_at: msg.created_at
              }
            });
          }

          if (msg.answer) {
            // AI response
            formatted.push({
              message: msg.answer,
              type: 'ai',
              metadata: {
                question: msg.question,
                created_at: msg.created_at,
                lnode: msg.lnode,
                urls: msg.urls,
                code: msg.code,
                code_instruction: msg.code_instruction
              }
            });
          }

          return formatted;
        });


        // Set the messages in state
        setFirstMessageSent(true)
        // console.log(formattedMessages)
        setChatMessages(formattedMessages);
      } else if (response.status === 401) {
        localStorage.removeItem("loggedin");
        navigate("/login?message=Session expired. Please log in again.");
      } else {
        console.error("Failed to fetch chat messages.");
      }
    } catch (error) {
      console.error("Error fetching chat messages:", error);
      navigate("/login?message=An error occurred. Please log in again.");
    } finally {
      setIsLoadingMessages(false);
    }
  };


  const sendMessage = async () => {
    if (message.trim() === '') return;

    if (!firstMessageSent) {
      const newChatId = chatid || await generateHash(id);
      setChatid(newChatId);
      setChatUrl(`${BASE_URL}/${newChatId}/`);
      navigate(`/chat/${id}/${newChatId}`);
      setFirstMessageSent(true);
    }

    setChatMessages(prevMessages => [
      ...prevMessages,
      { message, type: 'user' }
    ]);
    setIsSending(true);

    startStream();
    setMessage("")
  };

  const startStream = async () => {
    const idToken = localStorage.getItem("loggedin");

    try {
      const response = await fetch(`${CHAT_URL}?query=${message}&chat_id=${chatid}&is_memory=false`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${idToken}`,
          'Content-Type': 'application/json',
        }
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split('\n');

        for (let line of lines) {
          if (line.startsWith("data:")) {
            const cleanedData = line.replace(/^data:\s*/, '');
            console.log(cleanedData)
            try {
              // Parse top-level JSON
              const data = JSON.parse(cleanedData);
              console.log("data 1 = = = >", data)
              console.log("data.message.status = = = >", data.status)

              if (data.message && data.status && data.status.toLowerCase() === "done") {
                const parsedMessage = JSON.parse(data.message);


                // Clean and parse nested `response` field
                if (parsedMessage && parsedMessage.response) {

                  // const responseString = parsedMessage.response.replace(/\\"/g, '"').replace(/\\n/g, '');;

                  console.log("Parsed Response:", parsedMessage.response);

                  const formattedMessages = [
                    {
                      message: parsedMessage.response.answer,
                      type: 'ai',
                      metadata: {
                        question: parsedMessage.response.question,
                        created_at: new Date().toISOString(),
                        lnode: parsedMessage.response.lnode,
                        urls: parsedMessage.response.urls,
                        code: parsedMessage.response.code,
                        code_instruction: parsedMessage.response.code_instruction
                      }
                    }
                  ];

                  setChatMessages(prevMessages => [
                    ...prevMessages,
                    ...formattedMessages
                  ]);

                  setIsSending(false);
                  setReloadChatList(true);
                  setLastStep(""); // Reset last step

                }
              } else {
                console.log("")
                const parsedMessage = JSON.parse(data.message);

                console.log("cleanedMessage 2 = = = >", parsedMessage)
                setLastStep(parsedMessage.response.lnode || "Processing..."); // Update last step
              }
            } catch (error) {
              console.error("Error parsing JSON:", error);
            }
          }
        }

        // Clear the buffer up to the last newline to keep any remaining partial message
        buffer = buffer.slice(buffer.lastIndexOf('\n') + 1);
      }
    } catch (error) {
      console.error("Error with stream:", error);
    }
  };


  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      e.preventDefault();  // Prevents default Enter behavior
      sendMessage();
    }
    if (e.key === 'Enter') {
      e.preventDefault();
      if (lineCount < 3) {
        setLineCount(lineCount + 1);
        setFooterHeight(footerHeight + 5);
        setTextArea(textArea + 5);
      }
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileDetails(`${file.name} (${(file.size / 1024).toFixed(2)} KB)`);
    }
  };

  const handleChange = (e) => {
    setMessage(e.target.value);
  };

  const handleDeleteChat = async (chatId) => {
    try {
      const idToken = localStorage.getItem("loggedin");
      await fetch(`${BACKEND_URL}/api/chat_delete/${chatId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${idToken}`
        }
      });
      // Refresh chat list after deletion
      fetchChatList();
      setChatMessages([])
    } catch (error) {
      console.error("Error deleting chat:", error);
    }
  };
  return (
    <div className='chat-body chat-html'>
      <div className="chat-container">
        <div className="chat-row">
          <ChatNav userId={id} chatId={chatid} />
          <Await resolve={dataPromise.chatList} fallback={<p>Loading chat list...</p>}>
            <ChatHistory
              loginResponse={dataPromise.loginResponse}
              chatList={chatList}
              setChatid={setChatid}
              onDeleteChat={handleDeleteChat}
            />
          </Await>

          <section className="chat-chat">
            {isLoadingMessages ? (
              <p>Loading messages...</p>
            ) : (
              <Messages userId={id} chatId={chatid} messages={chatMessages} lastStep={lastStep} />
            )}
            <div className="chat-footer-chat" style={{ height: `${footerHeight}%` }}>
              <label htmlFor="file-upload">
                <FontAwesomeIcon className="chat-icon clickable" icon={faUpload} />
              </label>
              <input
                className='chat-send'
                id="file-upload"
                type="file"
                style={{ display: 'none' }}
                onChange={handleFileUpload}
              />
              <textarea
                type="text"
                className="chat-write-message"
                placeholder="Type your message here"
                rows={lineCount}
                style={{ height: `calc(${textArea}% - 20px)` }}
                onKeyDown={handleKeyPress}
                onChange={handleChange}
                value={fileDetails ? `${fileDetails}\n${message}` : message}
              />
              <FontAwesomeIcon
                className={`chat-icon chat-send clickable ${isSending ? 'disabled' : ''}`}
                onClick={!isSending ? sendMessage : null}
                icon={isSending ? faSpinner : faPaperPlane}
                spin={isSending}
              />
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
