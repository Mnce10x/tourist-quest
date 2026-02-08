const XLSX = require("xlsx");

// Sample polling data for a fictional election
const pollingData = [
  { Date: "2026-01-05", Pollster: "National Poll Group", CandidateA: 45, CandidateB: 42, CandidateC: 8, Undecided: 5, SampleSize: 1200, Region: "National" },
  { Date: "2026-01-08", Pollster: "Metro Research", CandidateA: 44, CandidateB: 43, CandidateC: 7, Undecided: 6, SampleSize: 800, Region: "National" },
  { Date: "2026-01-12", Pollster: "State Insights", CandidateA: 48, CandidateB: 40, CandidateC: 6, Undecided: 6, SampleSize: 600, Region: "North" },
  { Date: "2026-01-12", Pollster: "State Insights", CandidateA: 41, CandidateB: 46, CandidateC: 8, Undecided: 5, SampleSize: 600, Region: "South" },
  { Date: "2026-01-15", Pollster: "National Poll Group", CandidateA: 46, CandidateB: 41, CandidateC: 8, Undecided: 5, SampleSize: 1500, Region: "National" },
  { Date: "2026-01-18", Pollster: "DataPulse", CandidateA: 43, CandidateB: 44, CandidateC: 9, Undecided: 4, SampleSize: 1000, Region: "National" },
  { Date: "2026-01-20", Pollster: "State Insights", CandidateA: 50, CandidateB: 38, CandidateC: 7, Undecided: 5, SampleSize: 500, Region: "West" },
  { Date: "2026-01-20", Pollster: "State Insights", CandidateA: 42, CandidateB: 45, CandidateC: 7, Undecided: 6, SampleSize: 500, Region: "East" },
  { Date: "2026-01-22", Pollster: "Metro Research", CandidateA: 45, CandidateB: 42, CandidateC: 8, Undecided: 5, SampleSize: 900, Region: "National" },
  { Date: "2026-01-25", Pollster: "National Poll Group", CandidateA: 47, CandidateB: 41, CandidateC: 7, Undecided: 5, SampleSize: 1400, Region: "National" },
  { Date: "2026-01-28", Pollster: "DataPulse", CandidateA: 44, CandidateB: 43, CandidateC: 8, Undecided: 5, SampleSize: 1100, Region: "National" },
  { Date: "2026-01-30", Pollster: "State Insights", CandidateA: 49, CandidateB: 39, CandidateC: 6, Undecided: 6, SampleSize: 550, Region: "North" },
  { Date: "2026-01-30", Pollster: "State Insights", CandidateA: 40, CandidateB: 47, CandidateC: 8, Undecided: 5, SampleSize: 550, Region: "South" },
  { Date: "2026-02-01", Pollster: "Metro Research", CandidateA: 46, CandidateB: 41, CandidateC: 8, Undecided: 5, SampleSize: 950, Region: "National" },
  { Date: "2026-02-03", Pollster: "National Poll Group", CandidateA: 47, CandidateB: 40, CandidateC: 8, Undecided: 5, SampleSize: 1600, Region: "National" },
  { Date: "2026-02-05", Pollster: "DataPulse", CandidateA: 45, CandidateB: 42, CandidateC: 8, Undecided: 5, SampleSize: 1050, Region: "National" },
  { Date: "2026-02-05", Pollster: "State Insights", CandidateA: 51, CandidateB: 37, CandidateC: 7, Undecided: 5, SampleSize: 600, Region: "West" },
  { Date: "2026-02-05", Pollster: "State Insights", CandidateA: 43, CandidateB: 44, CandidateC: 7, Undecided: 6, SampleSize: 600, Region: "East" },
  { Date: "2026-02-07", Pollster: "Metro Research", CandidateA: 46, CandidateB: 41, CandidateC: 7, Undecided: 6, SampleSize: 1000, Region: "National" },
  { Date: "2026-02-08", Pollster: "National Poll Group", CandidateA: 48, CandidateB: 40, CandidateC: 7, Undecided: 5, SampleSize: 1800, Region: "National" },
];

// Historical election results
const historicalData = [
  { Year: 2018, PartyA: 48.2, PartyB: 45.1, Other: 6.7, Turnout: 62.5 },
  { Year: 2020, PartyA: 51.3, PartyB: 46.8, Other: 1.9, Turnout: 66.2 },
  { Year: 2022, PartyA: 47.8, PartyB: 49.5, Other: 2.7, Turnout: 58.1 },
  { Year: 2024, PartyA: 50.1, PartyB: 47.2, Other: 2.7, Turnout: 64.8 },
];

// Regional demographics
const regionData = [
  { Region: "National", Population: 50000000, RegisteredVoters: 35000000, HistoricalTurnout: 63.0 },
  { Region: "North", Population: 12000000, RegisteredVoters: 8400000, HistoricalTurnout: 65.2 },
  { Region: "South", Population: 14000000, RegisteredVoters: 9800000, HistoricalTurnout: 60.8 },
  { Region: "East", Population: 11000000, RegisteredVoters: 7700000, HistoricalTurnout: 61.5 },
  { Region: "West", Population: 13000000, RegisteredVoters: 9100000, HistoricalTurnout: 64.7 },
];

const wb = XLSX.utils.book_new();

const ws1 = XLSX.utils.json_to_sheet(pollingData);
XLSX.utils.book_append_sheet(wb, ws1, "Polling Data");

const ws2 = XLSX.utils.json_to_sheet(historicalData);
XLSX.utils.book_append_sheet(wb, ws2, "Historical Results");

const ws3 = XLSX.utils.json_to_sheet(regionData);
XLSX.utils.book_append_sheet(wb, ws3, "Regional Demographics");

XLSX.writeFile(wb, "election_data.xlsx");
console.log("Created election_data.xlsx");
