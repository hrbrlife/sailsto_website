// Home page — Life of a Deal: Mermaid init + story tab switching

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

function renderMermaidIn(container) {
    var nodes = container.querySelectorAll('.mermaid');
    nodes.forEach(function (node) {
        if (node.getAttribute('data-processed')) return;
    });
    mermaid.run({ nodes: Array.from(nodes) });
}

document.addEventListener('DOMContentLoaded', function () {
    var activePanel = document.querySelector('.story-panel.active');
    if (activePanel) renderMermaidIn(activePanel);

    var tabs = document.querySelectorAll('.story-tab');
    var panels = document.querySelectorAll('.story-panel');

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
            var target = tab.getAttribute('data-story');

            tabs.forEach(function (t) { t.classList.remove('active'); });
            tab.classList.add('active');

            panels.forEach(function (p) { p.classList.remove('active'); });
            var targetPanel = document.getElementById('story-' + target);
            if (targetPanel) {
                targetPanel.classList.add('active');
                renderMermaidIn(targetPanel);
                var storiesSection = document.getElementById('home-stories');
                if (storiesSection) {
                    storiesSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });
});
