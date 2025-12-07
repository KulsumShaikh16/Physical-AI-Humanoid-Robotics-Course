import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <h1 className={styles.heroTitle}>
          Physical AI & Humanoid Robotics
        </h1>
        <p className={styles.heroSubtitle}>
          Building the Future of Embodied Intelligence – From Theory to Practice
        </p>
        <div className={styles.buttons}>
          <Link
            className={clsx('button button--primary button--lg', styles.getStartedButton)}
            to="/docs/intro">
            Start Learning
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
      title: 'Production-Ready Systems',
      icon: '⚡',
      description: 'Deploy scalable robotics systems with modern DevOps practices, containerization, and cloud infrastructure.',
    },
    {
      title: 'Complete Learning Journey',
      icon: '📚',
      description: 'Comprehensive curriculum from programming fundamentals to deploying enterprise-grade robotic systems.',
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <h2 className={styles.featuresTitle}>What Makes This Book Different</h2>
        <p className={styles.featuresSubtitle}>
          A comprehensive, production-focused approach to co-learning Physical AI
        </p>
        <div className={styles.featureGrid}>
          {features.map((feature, idx) => (
            <div key={idx} className={styles.feature}>
              <div className={styles.featureIcon}>{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function MaturityLevels() {
  const levels = [
    {
      level: 'Level 1',
      title: 'AI Awareness',
      description: 'Understanding robotics fundamentals and AI concepts',
      color: '#FF6B6B',
    },
    {
      level: 'Level 2',
      title: 'AI Adoption',
      description: 'Using AI tools for robot development',
      color: '#FFA500',
    },
    {
      level: 'Level 3',
      title: 'AI Integration',
      description: 'Integrating AI into robotic systems',
      color: '#FFD700',
    },
    {
      level: 'Level 4',
      title: 'AI-Native Robots',
      description: 'Building robots with AI at their core',
      color: '#4ECDC4',
    },
    {
      level: 'Level 5',
      title: 'AI-First Enterprise',
      description: 'Deploying production robotics at scale',
      color: '#45B7D1',
    },
  ];

  return (
    <section className={styles.maturitySection}>
      <div className="container">
        <h2 className={styles.maturityTitle}>Learning Maturity Levels</h2>
        <div className={styles.maturityLevels}>
          {levels.map((level, idx) => (
            <div key={idx} className={styles.maturityLevel} style={{ borderLeftColor: level.color }}>
              <div className={styles.levelBadge} style={{ backgroundColor: level.color }}>
                {level.level}
              </div>
              <h3>{level.title}</h3>
              <p>{level.description}</p>
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
        <h2 className={styles.ctaTitle}>From Theory to Practice</h2>
        <h3 className={styles.ctaSubtitle}>From Learning to Building</h3>
        <p className={styles.ctaDescription}>
          Ready to build the future of Physical AI and Humanoid Robotics?
        </p>
        <Link
          className={clsx('button button--primary button--lg', styles.ctaButton)}
          to="/docs/intro">
          Begin Your Journey
        </Link>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics - Building the Future of Embodied Intelligence">
      <HomepageHeader />
      <main>
        <FeatureSection />
        <MaturityLevels />
        <CTASection />
      </main>
    </Layout>
  );
}
