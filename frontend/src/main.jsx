import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { ArrowRight, ArrowUpRight, Braces, Code2, Database, Github, Layers3, Linkedin, Menu, X } from 'lucide-react';
import { CareerPage, ContactPage } from './pages.jsx';
import './style.css';

const defaults = {
  name: 'Alan Shaju',
  headline: 'Building for the web.',
  intro: 'I’m Alan Shaju, a senior software engineer working across full-stack development and application architecture.',
  about: 'I’m interested in building web applications that feel considered from the interface through to the backend.',
  focus: 'Full stack · Application architecture',
  github: 'https://github.com/Alan2k2',
  linkedin: 'https://www.linkedin.com/in/alanshaju2k2/',
};

function post(path, body) {
  const token = document.cookie.split('; ').find(cookie => cookie.startsWith('csrftoken='))?.slice(10);
  return fetch('/api/' + path + '/', {
    method: 'POST',
    headers: { 'X-CSRFToken': token || '' },
    body,
    keepalive: path === 'visit',
  });
}

function ContactForm() {
  const [state, setState] = useState({});

  async function submit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    setState({ pending: true });
    try {
      const response = await post('contact', new FormData(form));
      const data = await response.json().catch(() => ({}));
      if (!response.ok || !data.ok) {
        throw new Error(Object.values(data.errors || {}).flat().join(' ') || 'Unable to send your message.');
      }
      form.reset();
      setState({ message: 'Thanks! Your message was received.' });
    } catch (error) {
      setState({ error: error.message });
    }
  }

  return <form onSubmit={submit} className="contact-form">
    <div className="fields">
      <label>Name<input name="name" placeholder="Your name" autoComplete="name" required maxLength={100} /></label>
      <label>Email<input name="email" type="email" placeholder="you@example.com" autoComplete="email" required maxLength={254} /></label>
    </div>
    <label>Message<textarea name="message" rows="5" placeholder="Tell me what’s on your mind" required maxLength={3000} /></label>
    <div hidden><label>Website<input name="website" tabIndex={-1} autoComplete="off" /></label></div>
    <button className="button primary" disabled={state.pending}>{state.pending ? 'Sending…' : 'Send message'} <ArrowRight size={17} /></button>
    <span role="status" className={state.error ? 'error' : ''}>{state.message || state.error}</span>
  </form>;
}

const navigation = [
  { label: 'Home', href: '/' },
  { label: 'Work', href: '/work/' },
  { label: 'Career', href: '/career/' },
  { label: 'Contact', href: '/contact/' },
];

function App() {
  const path = window.location.pathname.replace(/\/?$/, '/');
  const page = navigation.find(item => item.href === path) || navigation[0];
  const [data, setData] = useState({ profile: defaults, projects: [], experience: [] });
  const [query, setQuery] = useState('');
  const [menu, setMenu] = useState(false);
  const [privacy, setPrivacy] = useState(false);

  useEffect(() => {
    fetch('/api/content/').then(response => {
      if (!response.ok) throw new Error('Content unavailable');
      return response.json();
    }).then(setData).catch(() => {});
    const dnt = navigator.doNotTrack === '1' || navigator.globalPrivacyControl;
    if (!dnt && localStorage.getItem('portfolio-no-analytics') !== '1') {
      fetch('/api/csrf/').then(response => {
        if (!response.ok || localStorage.getItem('portfolio-no-analytics') === '1') return;
        return post('visit', new URLSearchParams({ referrer: document.referrer }));
      }).catch(() => {});
    }
  }, []);

  const { profile, projects, experience } = data;
  useEffect(() => {
    document.title = page.href === '/' ? `${profile.name} — Portfolio` : `${page.label} — ${profile.name}`;
  }, [page, profile.name]);
  const term = query.trim().toLowerCase();
  const displayedProjects = projects.filter(project =>
    [project.title, project.description, project.stack].some(value => value.toLowerCase().includes(term))
  );
  const initials = profile.name.trim().split(/\s+/).slice(0, 2).map(word => word[0]).join('');
  return <>
    <header className="header" id="top"><div className="wrap bar">
      <a className="brand" href="/"><span><Code2 size={20} /></span>{profile.name}</a>
      <button className="menu-toggle" aria-expanded={menu} aria-controls="navigation" aria-label={menu ? 'Close navigation' : 'Open navigation'} onClick={() => setMenu(!menu)}>{menu ? <X /> : <Menu />}</button>
      <nav id="navigation" className={menu ? 'open' : ''} aria-label="Main navigation">
        {navigation.map(item => <a
          className={item.href === '/contact/' ? 'nav-contact' : undefined}
          href={item.href}
          aria-current={page.href === item.href ? 'page' : undefined}
          key={item.href}
        >{item.label}{item.href === '/contact/' && <ArrowUpRight size={15} />}</a>)}
      </nav>
    </div></header>
    <main>
      {page.href === '/career/' && <CareerPage profile={profile} experience={experience} />}
      {page.href === '/contact/' && <ContactPage profile={profile}><ContactForm /></ContactPage>}
      {page.href === '/' && <>
      <section className="wrap hero">
        <div className="hero-copy">
          <div className="eyebrow"><span /> PERSONAL PORTFOLIO</div>
          <h1>{profile.headline}</h1>
          <p>{profile.intro}</p>
          <div className="actions"><a className="button primary" href="/work/">Explore my work <ArrowRight size={17} /></a><a className="button secondary" href={profile.github}><Github size={18} /> GitHub <ArrowUpRight size={15} /></a></div>
        </div>
        <div className="art" aria-hidden="true">
          <div className="art-top"><i /><i /><i /></div>
          <div className="orbit orbit-outer" /><div className="orbit orbit-inner" />
          <div className="monogram">{initials}<b>.</b></div>
          <div className="art-icon art-code"><Braces size={26} /></div><div className="art-icon art-db"><Database size={25} /></div>
          <div className="art-caption"><span /> {profile.focus}</div>
        </div>
      </section>
      <section className="wrap section home-links" aria-label="Explore the portfolio">
        <a className="project" id="work" href="/work/"><Layers3 size={24} aria-hidden="true" /><h2>Work</h2><p>Explore my public repositories and software projects.</p><ArrowUpRight size={19} aria-hidden="true" /></a>
        <a className="project" id="experience" href="/career/"><Braces size={24} aria-hidden="true" /><h2>Career</h2><p>See where I’ve worked and the roles I’ve held.</p><ArrowUpRight size={19} aria-hidden="true" /></a>
      </section>
      <section className="wrap section about" id="about">
        <div><div className="eyebrow"><span /> ABOUT</div><h2>Hi, I’m {profile.name}<span>.</span></h2></div>
        <div><p>{profile.about}</p><div className="tags"><Braces size={17} /> {profile.focus}</div><a className="text-link" href={profile.linkedin}><Linkedin size={18} /> Find me on LinkedIn <ArrowUpRight size={16} /></a></div>
      </section>
      <section className="wrap section page-next" id="contact">
        <h2>Let’s talk<span>.</span></h2>
        <a className="button primary" href="/contact/">Get in touch <ArrowRight size={17} /></a>
      </section>
      </>}
      {page.href === '/work/' &&
      <section className="wrap page-hero work-page">
        <div className="section-heading"><div><div className="eyebrow"><span /> WORK</div><h1>GitHub repositories.</h1></div><a className="text-link" href={profile.github}>View GitHub <ArrowUpRight size={17} /></a></div>
        {projects.length > 0 && <div className="project-toolbar">
          <label>Find a repository<input type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder="Search by name or technology" /></label>
          <p role="status">{displayedProjects.length} of {projects.length} repositories</p>
        </div>}
        <div className="projects">
          {projects.length ? displayedProjects.map(project => <article className="project" key={project.id}>
            <span className="tile-icon"><Layers3 size={24} /></span><h3>{project.title}</h3>{project.description && <p>{project.description}</p>}
            {project.stack && <div className="tags">{project.stack}</div>}
            {project.url && <a className="text-link" href={project.url}>View project <ArrowUpRight size={16} /></a>}
          </article>) : <article className="project project-empty"><span className="tile-icon"><Github size={27} /></span><div><h3>Explore my GitHub</h3><p>Browse my public repositories and follow what I’m working on.</p></div><a className="text-link" href={profile.github} aria-label="Explore my GitHub"><ArrowUpRight size={25} /></a></article>}
        </div>
        {projects.length > 0 && displayedProjects.length === 0 && <p>No repositories match your search.</p>}
      </section>
      }
    </main>
    <footer><div className="wrap footer">
      <a className="brand" href="/"><span><Code2 size={20} /></span>{profile.name}</a>
      <button className="plain" onClick={() => setPrivacy(!privacy)} aria-expanded={privacy}>Privacy</button>
      <div className="socials"><a href={profile.github} aria-label="GitHub"><Github size={21} /></a><a href={profile.linkedin} aria-label="LinkedIn"><Linkedin size={21} /></a></div>
      {privacy && <div className="privacy"><p>This site records visitor IP addresses, approximate location when available, browser user agent, preferred language, and referring site domain. Use the button below to disable future visit logging in this browser.</p><button className="button secondary" onClick={event => { localStorage.setItem('portfolio-no-analytics', '1'); event.currentTarget.textContent = 'Visit logging disabled'; }}>Disable visit logging</button></div>}
    </div></footer>
  </>;
}

createRoot(document.getElementById('root')).render(<App />);
