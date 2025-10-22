export interface Job {
  id: string;
  title: string;
  description: string;
  requirements: {
    must_have: string[];
    nice_to_have: string[];
  };
  status: 'active' | 'closed';
  created_at: string;
}

export interface Candidate {
  id: string;
  job_id: string;
  name: string;
  email: string;
  score: number;
  status: 'new' | 'reviewing' | 'accepted' | 'rejected';
  created_at: string;
}

export interface User {
  id: string;
  email: string;
  company_id: string;
  role: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
