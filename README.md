# Victor Sotero - Portfolio & CV

A modern, responsive portfolio website and CV for Victor Sotero, Senior Data Engineer.

## Features

- **Hero Section** with animated particle background
- **Interactive Experience Timeline** showcasing career progression
- **Skills Showcase** with visual proficiency indicators
- **Featured Projects** highlighting key achievements
- **Education & Certifications** section
- **Contact Form** with Netlify Forms integration
- **Dark/Light Theme** toggle with system preference detection
- **Printable CV** page optimized for PDF export
- **Fully Responsive** design for all devices

## Tech Stack

- **Static Site Generator**: [Hugo](https://gohugo.io/)
- **Animations**: [tsParticles](https://particles.js.org/)
- **Styling**: Custom CSS with CSS Variables
- **Hosting**: Netlify / Vercel

## Getting Started

### Prerequisites

- [Hugo](https://gohugo.io/installation/) (v0.121.0 or later)
- [Node.js](https://nodejs.org/) (v18 or later) - optional, for formatting

### Installation

```bash
# Clone the repository
git clone https://github.com/victorsotero/victor-website-cv.git
cd victor-website-cv

# Install formatting dependencies (optional)
npm install
```

### Development

```bash
# Start the development server
hugo server -D

# Or use npm script
npm run dev
```

The site will be available at `http://localhost:1313`

### Building for Production

```bash
# Build the site
hugo --gc --minify

# Or use npm script
npm run build
```

The built site will be in the `public/` directory.

## Project Structure

```
victor-website-cv/
├── archetypes/         # Content templates
├── content/            # Page content (Markdown)
│   ├── _index.md       # Home page
│   └── cv/             # CV page
├── data/
│   └── content.yaml    # Single source of truth for all content
├── layouts/
│   ├── _default/       # Base templates
│   ├── cv/             # CV page template
│   ├── partials/       # Reusable components
│   └── index.html      # Home page template
├── static/
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript files
├── config.toml         # Hugo configuration
├── netlify.toml        # Netlify deployment config
├── vercel.json         # Vercel deployment config
└── package.json        # Node.js dependencies
```

## Customization

### Content

All content is stored in `data/content.yaml`. Edit this file to update:

- Personal information
- Work experience
- Skills and technologies
- Education and certifications
- Projects

### Styling

The main stylesheet is located at `static/css/main.css`. It uses CSS custom properties (variables) for theming, making it easy to customize colors.

### Theme Colors

Edit the CSS variables in `:root`, `[data-theme="dark"]`, and `[data-theme="light"]` selectors to change the color scheme.

## Deployment

### Netlify

1. Push your code to GitHub
2. Connect your repository to Netlify
3. Netlify will automatically detect Hugo and deploy

### Vercel

1. Push your code to GitHub
2. Import your repository in Vercel
3. Set the framework preset to "Hugo"
4. Deploy

## CV / Print

Navigate to `/cv/` to view the printable CV. Click "Print / Save as PDF" or use `Ctrl/Cmd + P` to print or save as PDF.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
