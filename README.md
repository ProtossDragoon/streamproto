# StreamProto

StreamProto: High-Level Prototyping Component Sets Using Streamlit

## Requirements

- Python >= 3.9
- streamlit
- gspread

## Main Features

Streamlit is a web application framework for Python developers, designed for data-related tasks. However, there exists a gap between simple prototyping for visualization, such as in-house dashboards, and prototyping for public user testing.

A significant challenge in developing a basic web service with Streamlit is managing reusable code. Streamlit has a unique session management design. After every user interaction, Streamlit re-runs Python script files from the top, allowing data editing and frontend component rendering. Source code can become convoluted and challenging to maintain, primarily due to state management issues, without compromising application performance.

The goal of this repository is to provide additional features that minimize the need to delve into JavaScript, HTML, CSS, or backend frameworks unless they are absolutely necessary.

Key features include:
- Intuitive state manager for Streamlit sessions.
- Clean and easily readable code design
- Simple code examples provided for each module
- Modular design for gradual customization of assets (work in progress)
- Installation script (work in progress)

## streamail

![streamail](./docs/streamail-20f-200p.gif)

```bash
streamlit run src/streamail.py
```

## streamform

![streamform](./docs/streamform-20f-200p.gif)

```bash
streamlit run src/streamform.py
```

## streamsheet

![streamsheet](./docs/streamsheet-20f-200p.gif)

```bash
streamlit run src/streamsheet.py
```

### Requirements

- Create [Google SpreadSheet](https://docs.google.com/spreadsheets/) named `example-sheet`.
- Follow ['Enable API Access for a Project'](https://docs.gspread.org/en/v5.10.0/oauth2.html#enable-api-access-for-a-project) steps 1\~3 and ['Using Service Account'](https://docs.gspread.org/en/v5.10.0/oauth2.html#for-bots-using-service-account) steps 1\~8.
- Download service account json file and rename with `service-account.json`. Move the json file to this directory.
