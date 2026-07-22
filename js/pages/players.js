// Players page — Mermaid init + story tabs + scroll behaviour

mermaid.initialize({
    startOnLoad: false,
    theme: 'base',
    themeVariables: {
        primaryColor: '#3182ce',
        primaryTextColor: '#1a202c',
        primaryBorderColor: '#2c5282',
        lineColor: '#4a5568',
        secondaryColor: '#ebf8ff',
        tertiaryColor: '#f7fafc',
        nodeTextColor: '#1a202c',
        textColor: '#1a202c',
        labelTextColor: '#1a202c',
        edgeLabelBackground: '#ffffff',
        clusterBkg: '#e2e8f0',
        clusterBorder: '#a0aec0',
        titleColor: '#1a202c',
        actorTextColor: '#1a202c',
        actorLineColor: '#4a5568',
        signalTextColor: '#1a202c',
        labelBoxBkgColor: '#ebf8ff',
        labelBoxBorderColor: '#3182ce',
        noteBkgColor: '#fefcbf',
        noteTextColor: '#1a202c',
        noteBorderColor: '#d69e2e',
        actorBkg: '#ebf8ff',
        actorBorder: '#3182ce',
        sequenceNumberColor: '#fff'
    },
    flowchart: { curve: 'basis', padding: 20 },
    sequence: { mirrorActors: false, messageMargin: 40 }
});

// Render mermaid diagrams inside a specific container
function renderMermaidIn(container) {
    var nodes = container.querySelectorAll('.mermaid');
    nodes.forEach(function (node) {
        // Only render if not already rendered
        if (node.getAttribute('data-processed')) return;
        // mermaid.run expects an object with nodes array
    });
    mermaid.run({ nodes: Array.from(nodes) });
}

document.addEventListener('DOMContentLoaded', function () {
    // Render the active panel on load
    var activePanel = document.querySelector('.story-panel.active');
    if (activePanel) renderMermaidIn(activePanel);

    // Story tab switching
    var tabs = document.querySelectorAll('.story-tab');
    var panels = document.querySelectorAll('.story-panel');

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
            var target = tab.getAttribute('data-story');

            // Update tabs
            tabs.forEach(function (t) { t.classList.remove('active'); });
            tab.classList.add('active');

            // Update panels
            panels.forEach(function (p) { p.classList.remove('active'); });
            var targetPanel = document.getElementById('story-' + target);
            if (targetPanel) {
                targetPanel.classList.add('active');
                renderMermaidIn(targetPanel);
                // Scroll to the stories section
                var storiesSection = document.getElementById('stories');
                if (storiesSection) {
                    storiesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

    // Nav scroll highlight
    var nav = document.querySelector('nav');
    if (!nav) return;
    var scrollThreshold = 60;
    window.addEventListener('scroll', function () {
        if (window.scrollY > scrollThreshold) {
            nav.classList.add('nav-scrolled');
        } else {
            nav.classList.remove('nav-scrolled');
        }
    });
});
