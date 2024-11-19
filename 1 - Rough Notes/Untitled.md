2024-11-17 18:04

- to check port availability and usage use: 
`netstat -ano | findstr :8000`
- to terminate any conflicting processes use:
`taskkill /PID <PID> /F`
- to specifically check about the process use:
`tasklist /FI "PID eq <PID>"`  (use in cmd with administrative previlige)
  