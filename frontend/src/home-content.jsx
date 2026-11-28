import React from 'react';
import { ArrowUpRight, Braces, Layers3, Network, Smartphone } from 'lucide-react';

const specialties = [
  {
    icon: Braces,
    title: 'Full-stack applications',
    description: 'Building web interfaces, APIs, and content management systems.',
    tools: 'React · Django · Laravel',
  },
  {
    icon: Network,
    title: 'Application architecture',
    description: 'Designing modular frameworks and tooling for understanding how codebases fit together.',
    tools: 'PHP · Static analysis · APIs',
  },
  {
    icon: Smartphone,
    title: 'Mobile and integrations',
    description: 'Connecting mobile interfaces to backend services, databases, and mapping APIs.',
    tools: 'Flutter · Node.js · MongoDB',
  },
];

export function ProjectCard({ project }) {
  return <article className="project">
    <span className="tile-icon"><Layers3 size={24} aria-hidden="true" /></span>
    <h3>{project.title}</h3>
    {project.description && <p>{project.description}</p>}
    {project.stack && <p className="tags">{project.stack}</p>}
    {project.url && <a className="text-link" href={project.url}>View project <ArrowUpRight size={16} /></a>}
  </article>;
}

export function HomeContent({ projects, experience }) {
  return <>
    <section className="wrap section" aria-labelledby="specialties">
      <h2 id="specialties">What I build<span>.</span></h2>
      <div className="home-specialties">
        {specialties.map(({ icon: Icon, title, description, tools }) => <article className="specialty" key={title}>
          <span className="tile-icon"><Icon size={23} aria-hidden="true" /></span>
          <h3>{title}</h3>
          <p>{description}</p>
          <p className="tags">{tools}</p>
        </article>)}
      </div>
    </section>
    <section className="wrap section" id="work" aria-labelledby="home-work">
      <div className="section-heading">
        <h2 id="home-work">Selected projects<span>.</span></h2>
        <a className="text-link" href="/work/">Browse all repositories <ArrowUpRight size={17} /></a>
      </div>
      <div className="home-projects">
        {projects.slice(0, 3).map(project => <ProjectCard key={project.id} project={project} />)}
      </div>
    </section>
    <section className="wrap section home-career" id="experience" aria-labelledby="home-career">
      <div>
        <h2 id="home-career">Career highlights<span>.</span></h2>
        <a className="text-link" href="/career/">Explore the career timeline <ArrowUpRight size={17} /></a>
      </div>
      {experience.length > 0 && <ol className="home-roles">
        {experience.slice(0, 2).map(role => <li key={role.id}>
          {role.period && <span className="period">{role.period}</span>}
          <h3>{role.title}</h3>
          <p>{role.organization}</p>
          {role.location && <p>{role.location}</p>}
        </li>)}
      </ol>}
    </section>
  </>;
}
