import React, { useState } from 'react';
import { ArrowUpRight, BrainCircuit, Gamepad2, Grid2X2, Play } from 'lucide-react';
import './games.css';

const games = [
  {
    id: 'quiz',
    title: 'Quiz Club',
    genre: 'Trivia',
    description: 'Put your knowledge to the test with an interactive quiz.',
    url: 'https://quiz-club-565j.onrender.com/',
    icon: BrainCircuit,
  },
  {
    id: 'snake',
    title: 'Snake Arcade',
    genre: 'Classic arcade',
    description: 'Collect food, grow your snake, and try to beat your best score.',
    url: 'https://snake-arcade-n051.onrender.com/',
    icon: Grid2X2,
  },
];

export function GamesPage() {
  const [game, setGame] = useState(games[0]);

  return <div className="wrap games-page">
    <header className="games-hero">
      <div>
        <div className="eyebrow"><span /> OWN BUILT GAMES</div>
        <h1>The Arcade.</h1>
        <p>Two browser games I built. Pick a game to play here.</p>
      </div>
      <div className="arcade-art" aria-hidden="true">
        <div className="arcade-pad"><Gamepad2 size={68} strokeWidth={1.4} /></div>
      </div>
    </header>
    <div className="arcade-layout">
      <section className="game-picker" aria-labelledby="game-picker-title">
        <h2 id="game-picker-title">Choose a game</h2>
        {games.map(({ icon: Icon, ...option }, index) => <button
          key={option.id}
          className={`game-choice game-choice-${option.id}`}
          type="button"
          aria-pressed={game.id === option.id}
          aria-controls="game-player"
          onClick={() => setGame(games[index])}
        >
          <span className="game-icon"><Icon size={23} aria-hidden="true" /></span>
          <span><strong>{option.title}</strong><small>{option.genre}</small></span>
          <Play size={15} aria-hidden="true" />
        </button>)}
      </section>
      <section id="game-player" className="game-player" aria-labelledby="game-title">
        <div className="player-header">
          <div>
            <h2 id="game-title">{game.title}</h2>
            <p>{game.description}</p>
          </div>
          <a className="button secondary" href={game.url} target="_blank" rel="noopener noreferrer">
            Open in new tab <ArrowUpRight size={16} aria-hidden="true" />
          </a>
        </div>
        <iframe
          key={game.id}
          className="game-frame"
          src={game.url}
          title={`Play ${game.title}`}
          sandbox="allow-scripts allow-same-origin allow-forms allow-modals"
          allowFullScreen
          referrerPolicy="strict-origin-when-cross-origin"
        />
        <p className="player-note">If the game takes a moment to start or the player stays blank, open it in a new tab.</p>
      </section>
    </div>
  </div>;
}
