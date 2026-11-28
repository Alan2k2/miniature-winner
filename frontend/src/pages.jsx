import React from 'react';
import { ArrowRight, ArrowUpRight, BriefcaseBusiness, Github, Linkedin, MapPin, MessageSquare } from 'lucide-react';

export function CareerPage({ profile, experience }) {
  const latest = experience[0];
  return <>
    <section className="wrap page-hero career-hero">
      <div>
        <div className="eyebrow"><span /> CAREER</div>
        <h1>How I got here.</h1>
        <p>{profile.intro}</p>
      </div>
      {latest && <article className="career-feature">
        <BriefcaseBusiness size={24} aria-hidden="true" />
        <p className="feature-label">Most recent role</p>
        <h2>{latest.title}</h2>
        <p>{latest.organization}</p>
        {latest.period && <span className="period">{latest.period}</span>}
      </article>}
    </section>
    <section className="wrap section career-body" aria-labelledby="career-history">
      <div className="career-sidebar">
        <h2 id="career-history">Experience<span>.</span></h2>
        <p>{profile.focus}</p>
        <a className="text-link" href={profile.linkedin}><Linkedin size={17} /> View LinkedIn <ArrowUpRight size={16} /></a>
      </div>
      {experience.length ? <ol className="timeline">
        {experience.map(role => <li key={role.id}>
          <article className="role-card">
            {role.period && <span className="period">{role.period}</span>}
            <h3>{role.title}</h3>
            <p className="organization">{role.organization}</p>
            {role.location && <p className="location"><MapPin size={15} aria-hidden="true" />{role.location}</p>}
            {role.description && <p className="role-description">{role.description}</p>}
          </article>
        </li>)}
      </ol> : <p>Find my professional experience on LinkedIn.</p>}
    </section>
    <section className="wrap section page-next">
      <h2>Let’s work together<span>.</span></h2>
      <a className="button primary" href="/contact/">Get in touch <ArrowRight size={17} /></a>
    </section>
  </>;
}

export function ContactPage({ profile, children }) {
  return <section className="wrap page-hero contact-page">
    <div>
      <div className="eyebrow"><span /> CONTACT</div>
      <h1>Let’s talk.</h1>
      <p>Have a role, project, or collaboration in mind? Tell me a little about it and how I can reach you.</p>
      <div className="contact-links">
        <a href={profile.linkedin}><Linkedin size={20} /><span>LinkedIn</span><ArrowUpRight size={17} /></a>
        <a href={profile.github}><Github size={20} /><span>GitHub</span><ArrowUpRight size={17} /></a>
      </div>
    </div>
    <div className="contact-card">
      <span className="tile-icon"><MessageSquare size={23} aria-hidden="true" /></span>
      <h2>Send a message</h2>
      {children}
    </div>
  </section>;
}
