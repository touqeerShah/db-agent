import './AnalyticsInsights.css';
import attack from '../../assets/attack.png';

const AnalyticsInsights = () => {
  return (
    <section className="analytics-insights">
      <div className="analytics-insights-image">
        <figure className="analytics-image-container">
          <a href='https://github.com/Cyfrin/security-and-auditing-full-course-s23/tree/main?tab=readme-ov-file#top-attack-vectors'>
            <img
              src={attack}
              alt="Analytics Insights"
              className="image"
            />
          </a>
        </figure>
      </div>
      <div className="analytics-insights-content">
        <h3 className="insights-heading">Analytics Insights</h3>
        <ul className="insights-list">
          <li className="insight-item">
            <h4 className="insight-title">API Performance</h4>
            <p className="insight-description">
              Real-time metrics for optimal API performance. Monitor response times and optimize user experiences.
            </p>
          </li>
          <li className="insight-item">
            <div className="separator"></div>
            <h4 className="insight-title">Usage Trends</h4>
            <p className="insight-description">
              Analyze usage patterns for informed decision-making and employ data-driven insights to strategize effectively.
            </p>
          </li>
          <li className="insight-item">
            <div className="separator"></div>
            <h4 className="insight-title">Error Analysis</h4>
            <p className="insight-description">
              Identify and resolve issues with detailed error analytics. Enhance reliability by addressing potential bottlenecks.
            </p>
          </li>
        </ul>
      </div>
    </section>
  );
};

export default AnalyticsInsights;
