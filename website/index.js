import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import Post from './Post.js'
import PropTypes from 'prop-types';
import {fade, makeStyles} from '@material-ui/core/styles';
import IconButton from '@material-ui/core/IconButton';
import Drawer from "@material-ui/core/Drawer";
import Divider from "@material-ui/core/Divider";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import MenuIcon from '@material-ui/icons/Menu';
import CssBaseline from "@material-ui/core/CssBaseline";
import { createMuiTheme } from '@material-ui/core/styles';
import {MuiThemeProvider} from "@material-ui/core";
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import clsx from "clsx";

const drawerWidth = 300;

const theme = createMuiTheme({
  palette: {
    primary: { // works
      main: "#212121",
      contrastText: "#1de9b6",
    },
    secondary: { // works
      main: "#17a2bc",
      contrastText: "#1de9b6", //indigo[300]
    },

    third: { // works
      main: "#1de9b6",
      contrastText: "#1de9b6",
    },
  },
  typography:{
    fontSize: 13,
  },
  spacing:4,
});

const useStyles = makeStyles(theme => ({
  grow: {
    flexGrow: 1,
  },
  title: {
    display: 'none',
    [theme.breakpoints.up('sm')]: {
      display: 'block',
    },
  },
  sectionDesktop: {
    display: 'none',
    [theme.breakpoints.up('md')]: {
      display: 'flex',
    },
  },
  sectionMobile: {
    display: 'flex',
    [theme.breakpoints.up('md')]: {
      display: 'none',
    },
  },

  // From PermanentDrawer
  root: {
    display: 'flex'
  },
  appBar: {
    position:'fixed',
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    height: "65px",
  },
  appBarShift: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },

  menuButton: {
    marginRight: theme.spacing(2),
  },
  hide: {
    display: 'none',
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  // Drawer Setting
  drawerPaper: {
    background:"#424242",
    width: drawerWidth,
  },
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(0, 1),
    ...theme.mixins.toolbar,
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  contentShift: {
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    marginLeft: 0,
  },
  Title:{
    fontSize:20,
    fontWeight:600,
    marginLeft:30,
  },
  TitleLink:{
    fontSize:20,
    fontWeight:600,
    marginLeft:30,
    marginTop:20,
  },
  mainFeaturedPost: {
    position: 'relative',
    backgroundColor: theme.palette.grey[800],
    color: theme.palette.common.white,
    marginBottom: theme.spacing(4),
    backgroundImage: 'url(https://source.unsplash.com/random)',
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center',
  },
  overlay: {
    position: 'absolute',
    top: 0,
    bottom: 0,
    right: 0,
    left: 0,
    backgroundColor: 'rgba(0,0,0,.3)',
  },
  mainFeaturedPostContent: {
    position: 'relative',
    padding: theme.spacing(3),
    [theme.breakpoints.up('md')]: {
      padding: theme.spacing(6),
      paddingRight: 0,
    },
  },
}));



  const mainFeaturedPost = {
    title: "Malware Detection",
    image: 'markus-spiske-iar-afB0QQw-unsplash.jpg',
    imgText: 'main image description',
    linkText: 'Continue reading…',
  };

function App() {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);


  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);

  };

  return (
    <div>
        <MuiThemeProvider theme={theme}>
        <CssBaseline />
        <AppBar
          id="appbar"
          position="fixed"
          className={classes.appBar}
      >
        <Toolbar>
          <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={handleDrawerOpen}
              edge="start"
              className={clsx(classes.menuButton, {
                [classes.hide]: open,
              })}
          >
            <MenuIcon />
          </IconButton>

          <Typography className={classes.Title}>
                 (Title of Malware Paper)
          </Typography>

          </Toolbar>
          </AppBar>

          <Drawer
          className={classes.drawer}
          style={{width:drawerWidth}}
          variant="persistent"
          anchor="left"
          color="primary"
          open={open}
          classes={{
            paper: classes.drawerPaper,
          }}
      >
          <div className={classes.drawerHeader}>
            <IconButton onClick={handleDrawerClose}>
              {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
            </IconButton>
            <Typography className={classes.Title} style={{color:"#1de9b6"}} color="third">
                 Contents
          </Typography>
          </div>

          <Divider />

          <Typography className={classes.TitleLink} color="secondary">
                 <a href="#intro" style={{color:"#64b5f6", textDecoration:"none"}}> Background</a>
          </Typography>
          <Typography className={classes.TitleLink} color="secondary">
                 <a href="#method" style={{color:"#64b5f6", textDecoration:"none"}}> Methodology</a>
          </Typography>
        </Drawer>


        <Button variant="contained" color="primary">
            ""
        </Button>
        <div style={{margin:20}} ></div>
        <Post post={mainFeaturedPost}></Post>
        <main className={classes.content} style={{backgroundColor:"#1de9b6"}}>
        <Grid container color="primary" style={{marginBottom:20}}>
                <Grid item md={6} color="inherit"> 
                  <Paper className={classes.paper} color="secondary" style={{marginRight:70, textAlign:"center"}}>
                      Visual 1
                  </Paper>
                </Grid>
                <Grid item md={6} color="inherit"> 
                  <Paper className={classes.paper} color="secondary" style={{marginLeft:50, textAlign:"center"}}>
                    Visual 2
                  </Paper>
                </Grid>
          </Grid>
        <Paper className={classes.paper} color="secondary">

            <Typography paragraph id="intro" color="secondary">
                      Background:
            </Typography>
            <Typography paragraph id="intro" color="primary">
                      (Inner Part)
            </Typography>

        </Paper>

        <Grid container color="primary" style={{marginBottom:20}}>
                <Grid item md={6} color="inherit"> 
                  <Paper className={classes.paper} color="secondary" style={{marginRight:70, textAlign:"center"}}>
                      Figure 3
                  </Paper>
                </Grid>
                <Grid item md={6} color="inherit"> 
                  <Paper className={classes.paper} color="secondary" style={{marginLeft:50, textAlign:"center"}}>
                    Figure 4
                  </Paper>
                </Grid>
          </Grid>
        <Paper className={classes.paper} color="secondary">

            <Typography paragraph id="method" color="secondary">
                      Methodology:
            </Typography>
            <Typography paragraph id="method" color="primary">
                     <ol>
                        <li></li>
                        <li></li>
                        <li></li>
                     </ol>
            </Typography>
        </Paper>
        </main>

        </MuiThemeProvider>
    </div>
  );
}




//each are classes
//Classes:
    //.mainFeaturedPost
    //.overlay
    //.mainFreaturedPostContent


ReactDOM.render(<App />, document.getElementById('app'));
console.log("Hello?")