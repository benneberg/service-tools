// SignageOS Unlock StandAloneDevice Tool
(function () {
  document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('unlock_run');
    const copyBtn = document.getElementById('unlock_copy');
    const out = document.getElementById('unlock_output');

    if (!runBtn || !copyBtn || !out) return;

    runBtn.addEventListener('click', async () => {
      const deviceIp = document.getElementById('unlock_deviceIp').value.trim();
      const policyId = document.getElementById('unlock_policyId').value.trim();
      const orgId = document.getElementById('unlock_orgId').value.trim();
      const supportUser = document.getElementById('unlock_supportUser').value.trim();

      if (!deviceIp || !policyId) {
        out.textContent = '⚠️ Please fill Device IP and Policy ID.';
        return;
      }
      out.textContent = 'Running...';

      try {
        const resp = await fetch('/api/signageos/unlock', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ deviceIp, policyId, orgId, supportUser })
        });
        const data = await resp.json();
        if (resp.ok) {
          out.textContent = `✅ ${data.message}`;
        } else {
          out.textContent = `❌ ${data.message}`;
        }
      } catch (e) {
        out.textContent = `❌ Exception: ${e.message}`;
      }
    });

    copyBtn.addEventListener('click', () => {
      const deviceIp = document.getElementById('unlock_deviceIp').value.trim();
      const policyId = document.getElementById('unlock_policyId').value.trim();
      if (!deviceIp || !policyId) {
        showToast('error', 'Fill Device IP and Policy ID first');
        return;
      }
      // cURL uses placeholder for auth; instruct support to replace with real token or use the web app
      const curl = `curl -X POST "http://<HOST_OR_PROXY>/api/signageos/unlock" -H "Content-Type: application/json" -d '{"deviceIp":"${deviceIp}","policyId":"${policyId}","orgId":"<orgId_optional>","supportUser":"<you>"}'`;
      copyText(curl);
    });
  });
})();
