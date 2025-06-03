import './Banner.css'; // Create this file for styling
import banner from '../../assets/banner.png';

const Banner = () => {
  return (
    <>
      <section className="banner-outer-container">

        <section className="banner-container" id="hero">
          <section className="left-section">
            <div className="container">
              <div className="heading">
                <h3 className="sub-heading">API MANAGEMENT MADE EASY</h3>
              </div>
              <div className="main-heading">
                <h1>
                  Unmatched <span>scale</span> and <span>security</span>
                </h1>
              </div>
              <div className="spacer"></div>
              <div className="description">
                <p>
                  API management tool for crafting, overseeing, and securing APIs
                  across varied use cases, environments, and scales.
                </p>
              </div>
              <div className="spacer"></div>
              <div className="email-form-container">
                <form method="POST" className="email-form">
                  <input
                    type="email"
                    name="email"
                    placeholder="name@email.com"
                    className="email-input"
                    autoComplete="off"
                    autoCapitalize="off"
                    autoCorrect="off"
                    spellCheck="false"
                  />
                  <div className="submit-button-container">
                    <input type="submit" value="Join" className="submit-button" />
                  </div>
                </form>
              </div>
            </div>
          </section>

          <section className="right-section">
            <figure className="image-container">
              <img
                src={banner}
                alt="An abstract image that represents scalability"
                className="banner-image"
              />
            </figure>
          </section>
        </section>

      </section>
    </>
  );
};

export default Banner;
