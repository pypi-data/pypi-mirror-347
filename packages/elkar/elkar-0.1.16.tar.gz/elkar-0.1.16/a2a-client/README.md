## 🖥️ Elkar A2A Client

The Elkar A2A client is a React + TypeScript application for testing and interacting with A2A-compatible servers.

![Elkar A2A Client](../images/ui.png)


### 🔧 Features
- A2A Server debugging interface
    - Configure server URL
    - Send/Debug messages to A2A Servers with/without streaming
    - Debug task status and responses
    - Get task details by ID
    - Display artifacts returned by agents
- Task management for server agents
    - Register API keys for agents
    - Fast and easy integration in your agent server
    - Monitor task status and responses
    - Manage task history and artifacts
- Authentication using Supabase

### ✨ Managed Service
We also offer a managed version of the Elkar A2A platform at [app.elkar.co](https://app.elkar.co), providing a hassle-free way to leverage the full power of A2A communication without managing your own infrastructure.

Pre-requisites:
- Node.js (v18+)
- Supabase account (only for authentication): See [here](./SUPABASE_SETUP.md)
- For task management: Backend server running: See [here](https://github.com/elkar-ai/app)

### 🚀 Getting Started

1. **Install dependencies**
```bash
npm install
```

2. **Create a `.env` file**
```bash
cp .env.example .env
```

3. **Start the development server**
```bash
npm run dev
```

3. **Open your browser** at `http://localhost:5173`

### 🛠️ A2A Debugger-Only Mode

If you want to run the client purely for debugging A2A servers without setting up authentication or task management:

1. **Run in debugger-only mode**
```bash
npm run a2adebugger
```

2. **Open your browser** at `http://localhost:5173`

This mode provides a simplified interface focused solely on debugging A2A-compatible servers without requiring Supabase authentication or backend server integration.

### 📚 Usage
- Configure your A2A server URL and API key
- Send tasks and messages to agents
- Monitor task status and responses
- Manage task history and artifacts

### 🚧 Coming soon
- **Enhanced Server Authentication:** More robust and secure authentication methods for server interactions.
- **Hosted Agent Environment:** We will provide an environment to host agents for real-world testing scenarios, enabling complex interactions where an agent communicates with one or more other agents using the A2A protocol.
- **Push Notifications:** Real-time updates and notifications for task status changes and other important events.
- **Task Resubscription:** Ability to easily resubscribe to previously executed or failed tasks.

### ✨ Managed Service
We also offer a managed version of the Elkar A2A platform at [app.elkar.co](https://app.elkar.co), providing a hassle-free way to leverage the full power of A2A communication without managing your own infrastructure.

