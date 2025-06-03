import PropTypes from "prop-types";
import { useState } from "react";
import "./Header.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faTimes } from "@fortawesome/free-solid-svg-icons";
import { NavLink } from "react-router-dom";

const Header = ({ loginResponse }) => {
  const [isNavOpen, setIsNavOpen] = useState(false);

  const toggleNav = () => {
    setIsNavOpen(!isNavOpen);
  };

  return (
    <header className="header-container">
      <div className="header-content">
        <div className="logo">
          <img
            src="https://framerusercontent.com/images/20oeGq9SQ6t4N7faj9A9y5XjAg.png"
            alt="Solaris Logo"
          />
        </div>
        <button className="hamburger" onClick={toggleNav} aria-label="Toggle Navigation">
          <FontAwesomeIcon icon={faBars} />
        </button>

        <nav className={`nav-links ${isNavOpen ? "nav-active" : ""}`}>
          <button className="close-button nav-link" onClick={toggleNav} aria-label="Close Navigation">
            <FontAwesomeIcon icon={faTimes} />
          </button>
          <NavLink to="#overview" className="nav-link" onClick={toggleNav}>
            Overview
          </NavLink>
          <NavLink to="#features" className="nav-link" onClick={toggleNav}>
            Features
          </NavLink>
          <NavLink to="#references" className="nav-link" onClick={toggleNav}>
            References
          </NavLink>
          <NavLink to="#faq" className="nav-link" onClick={toggleNav}>
            FAQ
          </NavLink>

          {/* Consolidated Login/Chat Link */}
          <NavLink
            className=" nav-link"
            to={loginResponse.isLogin ? `/chat/${loginResponse.googleId}` : "/login"}
            onClick={toggleNav}
            end
          >
            {loginResponse.isLogin ? "Chat" : "Login"}
          </NavLink>
        </nav>

        {/* Demo button for larger screens, only one button with conditional path */}
        <NavLink
          className="waitlist-button desktop"
          to={loginResponse.isLogin ? `/chat/${loginResponse.googleId}` : "/login"}
          end
        >
          {loginResponse.isLogin ? "Chat" : "Login"}
        </NavLink>
      </div>

      {isNavOpen && <div className="overlay" onClick={toggleNav}></div>}
    </header>
  );
};

Header.propTypes = {
  loginResponse: PropTypes.shape({
    isLogin: PropTypes.bool.isRequired,
    googleId: PropTypes.string,
  }).isRequired,
};

export default Header;
