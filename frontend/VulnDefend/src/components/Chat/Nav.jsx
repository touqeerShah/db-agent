import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useNavigate } from "react-router-dom";

import { faHome, faUser, faComments, faFile, faCog, faRightFromBracket } from '@fortawesome/free-solid-svg-icons';
import { clearUserData } from "../../utils/storage";

const ChatNav = () => {
    const navigate = useNavigate();

    const logout = () => {
        clearUserData()
        navigate("/")
    }
    return <nav className="chat-menu">
        <ul className="chat-items">
            <li className="chat-item">
                <img
                    src="https://lh3.googleusercontent.com/a/ACg8ocLAkfZYV_JWjctchgvxAF3iLdGtuvwnf5KiKEHVV3Ahs5pCN13z1w=s96-c"
                    alt="User"
                    className="profile-image"
                />
            </li>
            <li className="chat-item">
                <FontAwesomeIcon icon={faHome} />
            </li>
            <li className="chat-item">
                <FontAwesomeIcon icon={faUser} />
            </li>
            <li className="chat-item item-active">
                <FontAwesomeIcon icon={faComments} />
            </li>
            <li className="chat-item">
                <FontAwesomeIcon icon={faFile} />
            </li>
            <li className="chat-item">
                <FontAwesomeIcon icon={faCog} />
            </li>
            <li className="chat-item"
                onClick={() => { logout() }}>

                <FontAwesomeIcon icon={faRightFromBracket} />
            </li>

        </ul>
    </nav>
}
export default ChatNav;
