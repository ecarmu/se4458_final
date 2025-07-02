/*import React from 'react';

import { BrowserRouter, Routes, Route } from 'react-router-dom';

import JobSearchHomePage from './pages/HomePage/JobSearchHomePage';
import SearchResultsPage from './pages/SearchResultPage/JobSearchResultPage';

export default function App() {
  return <div>Hello</div>;
}
  */


/*
import JobSearchHomePage from './pages/HomePage/JobSearchHomePage';
import SearchResultsPage from './pages/SearchResultPage/JobSearchResultPage';
import JobListing from './pages/JobPage/JobListing';

function App() {
  //return <JobSearchHomePage />;
  //return <SearchResultsPage />;
  return <JobListing />;
}

export default App;
*/

import { Routes, Route } from 'react-router-dom';
import JobSearchHomePage from './pages/HomePage/JobSearchHomePage';
import SearchResultsPage from './pages/SearchResultPage/JobSearchResultPage';
import JobListing from './pages/JobPage/JobListing';
import LoginRegisterPage from './pages/LoginRegisterPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<JobSearchHomePage />} />
      <Route path="/results" element={<SearchResultsPage />} />
      <Route path="/job/:id" element={<JobListing />} />
      <Route path="/auth" element={<LoginRegisterPage />} />
    </Routes>
  );
}

export default App;
