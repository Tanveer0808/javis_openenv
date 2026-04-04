document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.task-btn');
    const statusText = document.getElementById('sys-status');
    const terminal = document.getElementById('terminal-output');
    const nlpPanel = document.getElementById('nlp-panel');
    const nlpInput = document.getElementById('nlp-input');
    const nlpSubmitBtn = document.getElementById('nlp-submit');
    const progressFill = document.getElementById('progress-fill');

    let currentSessionId = null;
    let isAwaitingResponse = false;

    // Initialization bindings
    buttons.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            if (isAwaitingResponse) return;
            buttons.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            const taskName = e.target.getAttribute('data-task');
            await initInteractiveSession(taskName);
        });
    });

    async function initInteractiveSession(taskName) {
        isAwaitingResponse = true;
        terminal.innerHTML = '';
        addLog(`> Booting JARVIS Environment Core for [${taskName.toUpperCase()}]...`, 'system-msg');
        statusText.textContent = `INITIALIZING: ${taskName.toUpperCase()}`;
        statusText.className = 'status-running';

        try {
            const response = await fetch('/api/env/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ task: taskName })
            });
            const data = await response.json();
            
            if (response.ok) {
                currentSessionId = data.session_id;
                
                // Show NLP inputs
                nlpPanel.classList.remove('hidden');
                nlpInput.disabled = false;
                nlpSubmitBtn.disabled = false;
                progressFill.style.width = '0%';
                
                statusText.textContent = "AWAITING USER COMMAND";
                statusText.className = "status-online";
                
                addLog("> Environment Active. NLP Node listening...", "system-msg");
                const stateStr = JSON.stringify(data.state, null, 2);
                addLog(`<div class="state-box">${stateStr.replace(/\n/g, '<br>').replace(/ /g, '&nbsp;')}</div>`);
                
            } else {
                addLog(`> ERROR: ${data.error}`, 'reward-neg');
            }
        } catch (err) {
            addLog(`> Fetch Error: ${err}`, 'reward-neg');
        }
        isAwaitingResponse = false;
    }

    // Interactive NLP bindings
    nlpSubmitBtn.addEventListener('click', sendNlpCommand);
    nlpInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendNlpCommand();
    });

    async function sendNlpCommand() {
        if (!currentSessionId || isAwaitingResponse) return;
        const command = nlpInput.value.trim();
        if (!command) return;

        nlpInput.value = '';
        isAwaitingResponse = true;
        
        // Render user message natively
        addLog(`> USER POST: "${command}"`, "system-msg");
        
        try {
            const response = await fetch('/api/env/nlp_step', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ session_id: currentSessionId, input: command })
            });
            const data = await response.json();
            
            if(data.error) {
                addLog(`> Server Error: ${data.error}`, 'reward-neg');
            } else {
                const actionStr = JSON.stringify(data.action_parsed);
                addLog(`> JARVIS NLP PARSE EXECUTION: <span class="action-msg">${actionStr}</span>`);
                
                const rewardClass = data.reward >= 0 ? 'reward-pos' : 'reward-neg';
                const sign = data.reward >= 0 ? '+' : '';
                addLog(`  => REWARD: <span class="${rewardClass}">${sign}${data.reward}</span>`, "system-msg");

                // Update visual progress tracker!
                const progressVal = data.next_state.progress;
                progressFill.style.width = `${progressVal * 100}%`;
                if(progressVal >= 1.0) {
                    progressFill.style.boxShadow = "0 0 20px #00ff41";
                    progressFill.style.backgroundColor = "#00ff41";
                }

                const stateStr = JSON.stringify(data.next_state, null, 2);
                addLog(`<div class="state-box">${stateStr.replace(/\n/g, '<br>').replace(/ /g, '&nbsp;')}</div>`);

                if (data.done) {
                    addLog(`> Terminal condition verified! Final Academic Grade: ${data.final_score.toFixed(2)}`, 'system-msg glow-text');
                    nlpInput.disabled = true;
                    nlpSubmitBtn.disabled = true;
                    statusText.textContent = "PROTOCOL COMPLETE";
                    statusText.className = "status-success";
                }
            }
        } catch (err) {
            addLog(`> Communication Error: ${err}`, 'reward-neg');
        }
        
        scrollToBottom();
        isAwaitingResponse = false;
    }

    function addLog(html, className = '') {
        const div = document.createElement('div');
        if (className) div.className = `log-line ${className}`;
        div.innerHTML = html;
        terminal.appendChild(div);
        scrollToBottom();
    }

    function scrollToBottom() {
        terminal.scrollTop = terminal.scrollHeight;
    }
});
