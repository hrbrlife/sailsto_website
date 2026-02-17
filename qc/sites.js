/**
 * ═══════════════════════════════════════════════════════════════
 *   HRBR.LIFE PORTFOLIO — SITE CONFIGURATION
 * ═══════════════════════════════════════════════════════════════
 * 
 * Central configuration for all portfolio sites.
 * Each site entry tells the validators where to find content,
 * static files, layouts, glossary data, etc.
 */

const path = require('path');

const ROOT = path.join(__dirname, '..');

const SITES = {
    sailsto: {
        name: 'Sails.to',
        domain: 'sails.to',
        type: 'hugo',
        dir: path.join(ROOT, 'hugo-site'),
        contentDirs: [
            path.join(ROOT, 'hugo-site', 'content'),
        ],
        layoutDirs: [
            path.join(ROOT, 'hugo-site', 'layouts'),
        ],
        staticDirs: [
            path.join(ROOT, 'hugo-site', 'static'),
        ],
        publicDir: path.join(ROOT, 'hugo-site', 'public'),
        glossary: {
            json: path.join(ROOT, 'hugo-site', 'static', 'assets', 'content', 'glossary.json'),
            pagesDir: path.join(ROOT, 'hugo-site', 'content', 'knowledge', 'glossary'),
        },
        devServer: 'http://localhost:1313',
        fileExtensions: ['.md', '.html'],
    },

    kyclat: {
        name: 'KYC.lat',
        domain: 'kyc.lat',
        type: 'vite',
        dir: path.join(ROOT, 'kyclat_website'),
        contentDirs: [
            path.join(ROOT, 'kyclat_website', 'content'),
            path.join(ROOT, 'kyclat_website', 'src'),
        ],
        layoutDirs: [
            path.join(ROOT, 'kyclat_website', 'src'),
        ],
        staticDirs: [
            path.join(ROOT, 'kyclat_website', 'public'),
        ],
        publicDir: path.join(ROOT, 'kyclat_website', 'public'),
        glossary: {
            contentDir: path.join(ROOT, 'kyclat_website', 'content', 'glossary'),
            format: 'json-per-file',
        },
        devServer: 'http://localhost:5173',
        fileExtensions: ['.json', '.tsx', '.ts', '.html'],
    },

    melusina: {
        name: 'Melusina-OS.org',
        domain: 'melusina-os.org',
        type: 'vite',
        dir: path.join(ROOT, 'melusina-os'),
        contentDirs: [
            path.join(ROOT, 'melusina-os', 'content'),
            path.join(ROOT, 'melusina-os', 'src'),
        ],
        layoutDirs: [
            path.join(ROOT, 'melusina-os', 'src'),
        ],
        staticDirs: [
            path.join(ROOT, 'melusina-os', 'public'),
        ],
        publicDir: path.join(ROOT, 'melusina-os', 'public'),
        glossary: {
            contentDir: path.join(ROOT, 'melusina-os', 'content', 'glossary'),
            format: 'json-per-file',
        },
        devServer: 'http://localhost:5174',
        fileExtensions: ['.json', '.tsx', '.ts', '.html'],
    },

    instakycapp: {
        name: 'InstaKYC',
        domain: 'instakyc.app',
        type: 'vite',
        dir: path.join(ROOT, 'INSTAKYCAPP_WEBSITE'),
        contentDirs: [
            path.join(ROOT, 'INSTAKYCAPP_WEBSITE', 'content'),
            path.join(ROOT, 'INSTAKYCAPP_WEBSITE', 'src'),
        ],
        layoutDirs: [
            path.join(ROOT, 'INSTAKYCAPP_WEBSITE', 'src'),
        ],
        staticDirs: [
            path.join(ROOT, 'INSTAKYCAPP_WEBSITE', 'public'),
        ],
        publicDir: path.join(ROOT, 'INSTAKYCAPP_WEBSITE', 'public'),
        glossary: {
            contentDir: path.join(ROOT, 'INSTAKYCAPP_WEBSITE', 'content', 'glossary'),
            format: 'json-per-file',
        },
        devServer: 'http://localhost:5175',
        fileExtensions: ['.json', '.tsx', '.ts', '.html'],
    },

    hrbr: {
        name: 'HRBR.LIFE',
        domain: 'hrbr.life',
        type: 'static',
        dir: path.join(ROOT, 'hrbrlife_website'),
        contentDirs: [
            path.join(ROOT, 'hrbrlife_website'),
        ],
        layoutDirs: [],
        staticDirs: [
            path.join(ROOT, 'hrbrlife_website'),
        ],
        publicDir: path.join(ROOT, 'hrbrlife_website'),
        glossary: null,
        devServer: null,
        fileExtensions: ['.html'],
    },

    // ─── Coming-soon sites ──────────────────────────────────

    aitxpro: {
        name: 'AITX.pro',
        domain: 'aitx.pro',
        type: 'static',
        dir: path.join(ROOT, 'aitxpro_site'),
        contentDirs: [path.join(ROOT, 'aitxpro_site')],
        layoutDirs: [],
        staticDirs: [path.join(ROOT, 'aitxpro_site')],
        publicDir: path.join(ROOT, 'aitxpro_site'),
        glossary: null,
        devServer: null,
        fileExtensions: ['.html'],
    },

    ccash: {
        name: 'CCA.sh',
        domain: 'cca.sh',
        type: 'static',
        dir: path.join(ROOT, 'ccash_site'),
        contentDirs: [path.join(ROOT, 'ccash_site')],
        layoutDirs: [],
        staticDirs: [path.join(ROOT, 'ccash_site')],
        publicDir: path.join(ROOT, 'ccash_site'),
        glossary: null,
        devServer: null,
        fileExtensions: ['.html'],
    },

    freecoapp: {
        name: 'FreeCo.app',
        domain: 'freeco.app',
        type: 'static',
        dir: path.join(ROOT, 'freecoapp_site'),
        contentDirs: [path.join(ROOT, 'freecoapp_site')],
        layoutDirs: [],
        staticDirs: [path.join(ROOT, 'freecoapp_site')],
        publicDir: path.join(ROOT, 'freecoapp_site'),
        glossary: null,
        devServer: null,
        fileExtensions: ['.html'],
    },

    instadao: {
        name: 'InstaDAO.app',
        domain: 'instadao.app',
        type: 'static',
        dir: path.join(ROOT, 'instadao_site'),
        contentDirs: [path.join(ROOT, 'instadao_site')],
        layoutDirs: [],
        staticDirs: [path.join(ROOT, 'instadao_site')],
        publicDir: path.join(ROOT, 'instadao_site'),
        glossary: null,
        devServer: null,
        fileExtensions: ['.html'],
    },

    instatrust: {
        name: 'InstaTrust.app',
        domain: 'instatrust.app',
        type: 'static',
        dir: path.join(ROOT, 'instatrust_site'),
        contentDirs: [path.join(ROOT, 'instatrust_site')],
        layoutDirs: [],
        staticDirs: [path.join(ROOT, 'instatrust_site')],
        publicDir: path.join(ROOT, 'instatrust_site'),
        glossary: null,
        devServer: null,
        fileExtensions: ['.html'],
    },
};

module.exports = { SITES, ROOT };
