import React, { useEffect, useContext } from "react";
import texhIng from "../../image/tech.jpg";
import reactLogo from "../../image/react.png";
import nodeLogo from "../../image/node.png";
import pythonLogo from "../../image/python.png";
import pusherLogo from "../../image/pusher.png";
import tensorflow from "../../image/tensorflow.png";
import mongodbLogo from "../../image/mongodb.png";
import Inspiration from "../../image/Inspiration.png";
import M from "materialize-css/dist/js/materialize.min.js";
import FadeIn from "react-fade-in";
import ContactContaxt from "../../context/contact/contactContext";
import Aos from "aos";
import "aos/dist/aos.css";

export const About = () => {
  const contactContext = useContext(ContactContaxt);
  useEffect(() => {
    //Init Materialize JS
    M.AutoInit();
    Aos.init({ duration: 2500 });
    contactContext.setPage("about");
  }, []);

  return (
    <div>
      <FadeIn>
        <section className="section section-icons center">
          <div className="container">
            <div className="row">
              <br />

              <div className="col s12 m4">
                <div className="card-panel">
                  <i className="fab fa-discord fa-3x deep-purple-text text-darken-2"></i>
                  <h5 className="grey-text text-darken-4">Free Access</h5>
                  <p>
                    Pump Bot is completely free and sends out an alert to
                    Discord server regrading the listing
                  </p>
                  <br />
                  <br />
                </div>
              </div>
              <div className="col s12 m4">
                <div className="card-panel">
                  <i className="fa fa-database fa-3x deep-purple-text text-darken-2"></i>
                  <h5 className="grey-text text-darken-4">NoSQL Databases</h5>
                  <p>
                    Pump Bot is also available on Web Application and connected
                    to NoSQL databse which allow user to view pump & dump alert
                  </p>
                  <br />
                </div>
              </div>
              <div className="col s12 m4">
                <div className="card-panel">
                  <i className="fa fa-bolt fa-3x deep-purple-text text-darken-2"></i>
                  <h5 className="grey-text text-darken-4">Always up to date</h5>
                  <p>
                    Pump Bot uses Pusher technology which allow us to communicat
                    to the server in real-time and collect the most up to date
                    data
                  </p>
                  <br />
                </div>
              </div>
            </div>
          </div>
        </section>
      </FadeIn>

      <section
        data-aos="fade-right"
        class="section section-testimonial grey lighten-4"
      >
        <div class="">
          <div class="row">
            <div class="col s12">
              <section class="section section-about grey lighten-4">
                <div className="container">
                  <div className="row">
                    <div className="col s12 m6">
                      <h3>
                        About
                        <span class="deep-purple-text text-darken-1 ">
                          {" "}
                          Pumb Bot
                        </span>
                      </h3>

                      <p className="">
                        Pumb Bot is a machine learning cryptocurrency robot
                        which detects and sends alerts about pump & dump schemes
                        on cryptocurrency exchanges and stock markets. This
                        program is meant to run on a server and send out alerts
                        when it detects a pump & dump. The program is built
                        using Python 3.6.
                      </p>
                    </div>
                    <div className="col s12 m6">
                      <img
                        src={texhIng}
                        className="circle responsive-img aboutImag"
                      />
                    </div>
                  </div>
                </div>
              </section>
            </div>
          </div>
        </div>
      </section>

      <section
        data-aos="fade-left"
        class="section section-testimonial  lighten-4"
      >
        <div class="">
          <br />
          <div class="row">
            <div class="col s12">
              <section class="section section-about  lighten-4">
                <div className="container">
                  <div className="row">
                    <div className="col s12 m6">
                      <img
                        src={Inspiration}
                        className="circle responsive-img  aboutImag"
                      />
                    </div>
                    <div className="col s12 m6">
                      <h3>
                        Our
                        <span class="deep-purple-text text-darken-1 ">
                          {" "}
                          Inspiration
                        </span>
                      </h3>

                      <p className="">
                        This project is meant to expand on research on
                        cryptocurrency pump & dumps, which is an emerging
                        problem in the field of criminal science. Specifically,
                        this project is a continuation of the research done by
                        Josh Kamps and Bennett Kleinberg of University College
                        London on cryptocurrency pump & dumps. (Kamps, J;
                        Kleinberg, B; (2018) To the moon: defining and detecting
                        cryptocurrency pump-and-dumps. Crime Science, 7, Article
                        18.)
                      </p>
                    </div>
                  </div>
                </div>
              </section>
            </div>
          </div>
        </div>
        <br />
      </section>

      <section
        className="section section-developers white-text"
        style={{ marginTop: "-40px" }}
      >
        <div className="primary-overlay valign-wrapper">
          <div className="row">
            <div className="col s12 center">
              <h2 className="dataText">Collect Data and See The Future</h2>
            </div>
          </div>
        </div>
      </section>
      <section className="section section-language  lighten-4">
        <br />
        <div className="container">
          <br />
          <br />

          <br />
          <br />

          <div className="row">
            <h3 data-aos="fade-in" className="center">
              <span className="deep-purple-text text-darken-1">
                Technology{" "}
              </span>
              We Use
            </h3>
            <br />
            <br />
            <br />
            <br />
            <div className="row">
              <div className="col m2 s2">
                <img
                  data-aos="fade-up"
                  src={pusherLogo}
                  className="responsive-img"
                />
              </div>
              <div className="col m2 s2">
                <img
                  data-aos="fade-down"
                  src={reactLogo}
                  className="responsive-img"
                />
              </div>
              <div className="col m2 s2">
                <img
                  data-aos="fade-up"
                  src={tensorflow}
                  className="responsive-img"
                />
              </div>
              <div className="col m2 s2">
                <img
                  data-aos="fade-down"
                  src={nodeLogo}
                  className="responsive-img"
                />
              </div>
              <div className="col m2 s2">
                <img
                  data-aos="fade-up"
                  src={mongodbLogo}
                  className="responsive-img"
                />
              </div>
              <div className="col m2 s2">
                <img
                  data-aos="fade-down"
                  src={pythonLogo}
                  className="responsive-img"
                />
              </div>
            </div>
            <br />
            <br />
            <br />
            <br />
          </div>
        </div>

        <br />
      </section>

      <section className="section section-how white-text">
        <div className="primary-overlay2 valign-wrapper">
          <div className="row">
            <div className="col s12 center">
              <h2>Seeing The Future</h2>
            </div>
          </div>
        </div>
      </section>

      <section className="section section-features  lighten-3">
        <br />
        <div className="container">
          <h3 data-aos="fade-in" className="purple-text text-darken-1 center">
            Powerful & Innovative Functionality{" "}
          </h3>
          <h6 data-aos="fade-in" className="grey-text text-darken-2 center">
            Combining Machine Learning With Financial Stock Market
          </h6>
          <br />
          <br />
          <div className="row">
            <div data-aos="fade-right" className="col s12 m6">
              <h4>
                <i className="fab fa-btc"></i> Cryptocurrency Data
              </h4>
              <p>
                We are using APIs specific to each cryptocurrency exchange we
                analyze in order to obtain price and volume data. For example,
                cryptocurrency listings on Binance are obtained with the Binance
                API. Using exchange-specific APIs allows us to obtain accurate,
                real-time, minute specific information on each coin. When the
                program starts, it downloads a list of all coins on the exhange
                and keeps them updated in a database.
              </p>
            </div>
            <div data-aos="fade-left" className="col s12 m6">
              <h4>
                <i className="fab fa-discord"></i> Discord
              </h4>
              <p>
                After a pump & dump is detected, a Discord bot sends out an
                alert to a Discord server regarding the listing. The bot runs
                concurrently with the program and is optional. This bot uses
                Discord.py.
              </p>
            </div>
          </div>
          <div className="row">
            <div data-aos="fade-right" className="col s12 m6">
              <h4>
                <i className="fa fa-hdd"></i> TensorFlow
              </h4>
              <p>
                We are using custom TensorFlow-powered classification neural
                networks to interpret the real-time data of listings. The
                network outputs a single probability - the probability that the
                stock is beginning to experience a pump & dump. The input layer
                accepts the most recent price changes of a penny stock. The
                output layer contains a single output node with our probability.
                Our training data is custom-made. We are willing to sacrifice
                some recall for higher precision. Note that this program uses
                TensorFlow 2, which currently supports up to Python 3.6 (as of
                April 20th, 2020).
              </p>
            </div>
            <div data-aos="fade-left" className="col s12 m6">
              <h4>
                <i className="fa fa-chart-line"></i> Stock Data
              </h4>
              <p>
                In addition to cryptocurrency, our program is also built to
                analyze stock market data. The program first downloads all
                listings from relevant markets (e.g. NASDAQ, TSX), usually via
                FTP. Afterwards, the program filters out the listings that are
                not penny stocks. Only penny stocks are stored because pump &
                dump stock schemes typically occur with penny stocks, and not
                high-value stocks. As with cryptocurrency listings, the program
                keeps the prices of penny stock listings up-to-date as it runs.
                Currently, stock listing prices are obtained with the yfinance
                library.
              </p>
            </div>
          </div>
        </div>
        <br />
        <div data-aos="fade-up" className="center">
          <a
            href="https://github.com/Robert-Ciborowski/PumpBot"
            className="btn btn-large grey"
          >
            Check Out The Product
          </a>
        </div>
      </section>
    </div>
  );
};

export default About;
