import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch, faTrashAlt } from '@fortawesome/free-solid-svg-icons';

const ChatHistory = ({ loginResponse, chatList, setChatid, onDeleteChat }) => {
    const { isLogin } = loginResponse;
    console.log("chatList", chatList)
    // Function to calculate how many days old the chat is
    const calculateDaysOld = (updatedAt) => {
        const updatedDate = new Date(updatedAt);
        const today = new Date();
        const diffTime = Math.abs(today - updatedDate);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays;
    };

    const changeChat = (chat_id) => {
        setChatid(chat_id);
    };

    return (
        <section className="chat-discussions">
            {isLogin ? (
                <>
                    <div className="chat-discussion chat-search">
                        <div className="chat-searchbar">
                            <FontAwesomeIcon icon={faSearch} />
                            <input type="text" placeholder="Search..." />
                        </div>
                    </div>

                    {chatList && chatList.results.length > 0 ? (
                        chatList.results.map((chat) => (
                            <div
                                key={chat.chat_id}
                                className="chat-discussion message-active"
                                onClick={() => changeChat(chat.chat_id)}
                            >
                                <div className="chat-desc-contact">
                                    <p className="chat-name">{chat.title || "Chat Title"}</p>
                                </div>
                                <div className="chat-timer">
                                    {`${calculateDaysOld(chat.updated_at)} day(s) old`}                                    <button
                                        className="delete-button"
                                        onClick={(e) => {
                                            e.stopPropagation(); // Prevent triggering changeChat on delete
                                            onDeleteChat(chat.chat_id);
                                        }}
                                    >
                                        <FontAwesomeIcon icon={faTrashAlt} />
                                    </button>
                                </div>
                            </div>
                        ))
                    ) : (
                        <p>No chats available.</p>
                    )}
                </>
            ) : (
                <p>Please log in to view your chat history.</p>
            )}
        </section>
    );
};

ChatHistory.propTypes = {
    loginResponse: PropTypes.shape({
        isLogin: PropTypes.bool.isRequired,
        googleId: PropTypes.string
    }).isRequired,
    chatList: PropTypes.shape({
        results: PropTypes.arrayOf(
            PropTypes.shape({
                chat_id: PropTypes.string.isRequired,
                title: PropTypes.string,
                updated_at: PropTypes.string.isRequired
            })
        ).isRequired,
        current_page: PropTypes.number,
        total_pages: PropTypes.number,
        total_chats: PropTypes.number,
        has_next: PropTypes.bool,
        has_previous: PropTypes.bool
    }).isRequired
    ,
    setChatid: PropTypes.func,
    onDeleteChat: PropTypes.func.isRequired
};

export default ChatHistory;
