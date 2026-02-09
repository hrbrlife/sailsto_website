// Players page — Mermaid init + scroll behaviour

mermaid.initialize({
    startOnLoad: true,
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

// Smooth-scroll nav highlight
document.addEventListener('DOMContentLoaded', function () {
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
