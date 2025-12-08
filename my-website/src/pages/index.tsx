import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero-title">
          {siteConfig.title}
        </Heading>
        <p className="hero-subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Reading
          </Link>
          <Link
            className="button button--secondary button--lg glass-panel"
            to="https://github.com/KulsumShaikh16/Physical-AI-Humanoid-Robotics-Course">
            View on GitHub
          </Link>
        </div>
      </div>
    </header>
  );
}

function FeatureSection() {
  const features = [
    {
      title: 'Co-Learning Philosophy',
      icon: '🤝',
      description: 'Learn alongside AI agents. Not just using AI as a tool, but co-creating where both human and AI learn together.',
    },
    {
      title: 'Embodied Intelligence',
      icon: '🤖',
      description: 'Explore physical AI systems that interact with the real world through sensors, actuators, and intelligent control.',
    },
    {
      title: 'Humanoid Robotics',
      icon: '🦾',
      description: 'Build and program humanoid robots with advanced perception, manipulation, and navigation capabilities.',
    },
    {
      title: 'Reinforcement Learning',
      icon: '🎯',
      description: 'Master RL algorithms for training autonomous agents in simulated and real-world environments.',
    },
    {
      title: 'Production-Ready',
      icon: '⚡',
      description: 'Deploy scalable robotics systems with modern DevOps practices, containerization, and cloud infrastructure.',
    },
    {
      title: 'Full Stack Journey',
      icon: '📚',
      description: 'Comprehensive curriculum from programming fundamentals to deploying enterprise-grade robotic systems.',
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <h2 className={styles.featuresTitle}>Why This Book?</h2>
        <div className={styles.featureGrid}>
          {features.map((feature, idx) => (
            <div key={idx} className={clsx('card feature-card', styles.feature)}>
              <div className="card__header">
                <h3>{feature.icon} {feature.title}</h3>
              </div>
              <div className="card__body">
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function MaturityLevels() {
  const levels = [
    { level: 'Level 1', title: 'AI Awareness', desc: 'Foundations of Robotics & AI' },
    { level: 'Level 2', title: 'AI Adoption', desc: 'Using AI Tools for Development' },
    { level: 'Level 3', title: 'AI Integration', desc: 'Embedding AI in Robot Systems' },
    { level: 'Level 4', title: 'AI-Native Robots', desc: 'Autonomous Agents at the Core' },
    { level: 'Level 5', title: 'AI-First Enterprise', desc: 'Scale & Production Deployment' },
  ];

  return (
    <section className={styles.maturitySection}>
      <div className="container">
        <h2 className={styles.featuresTitle}>Learning Maturity Path</h2>
        <div className={styles.maturityLevels}>
          {levels.map((lvl, idx) => (
            <div key={idx} className={styles.maturityLevel}>
              <div className={styles.levelBadge}>{lvl.level}</div>
              <div>
                <h3 style={{ margin: 0 }}>{lvl.title}</h3>
                <p style={{ margin: 0, opacity: 0.7 }}>{lvl.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.ctaSection}>
      <div className="container">
        <h2 className={styles.ctaTitle}>Ready to Build?</h2>
        <p className={styles.ctaDescription}>
          Join the revolution of Physical AI and start building intelligent humanoid robots today.
        </p>
        <Link
          className="button button--primary button--lg"
          to="/docs/intro">
          Start Learning Now
        </Link>
      </div>
    </section>
  );
}

export default function Home(): React.JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="Physical AI & Humanoid Robotics - Shaping the Future of Robotics: Bridging Intelligent Systems with the Physical World. Empowering the Next Generation of AI-Driven Humanoid Robots for Real-World Applications.">
      <HomepageHeader />
      <main>
        <FeatureSection />
        <MaturityLevels />
        <CTASection />
      </main>
    </Layout>
  );
}


