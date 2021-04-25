const LoadingIcon = () => {
  return (
    <div className="spinner">
      <div className="rect1"></div>
      <div className="rect2"></div>
      <div className="rect3"></div>
      <div className="rect4"></div>
      <div className="rect5"></div>
      <style jsx>
        {`
          .spinner {
            margin: 100px auto;
            width: 50px;
            height: 40px;
            text-align: center;
            font-size: 10px;
            // font-family: sans-serif;
          }

          .spinner > div {
            background-color: #333;
            margin: 0 3px 0 0;
            height: 100%;
            width: 6px;
            display: inline-block;

            -webkit-animation: sk-stretchdelay 1.2s infinite ease-in-out;
            animation: sk-stretchdelay 1.2s infinite ease-in-out;
          }

          .spinner .rect2 {
            -webkit-animation-delay: -1.1s;
            animation-delay: -1.1s;
          }

          .spinner .rect3 {
            -webkit-animation-delay: -1s;
            animation-delay: -1s;
          }

          .spinner .rect4 {
            -webkit-animation-delay: -0.9s;
            animation-delay: -0.9s;
          }

          .spinner .rect5 {
            -webkit-animation-delay: -0.8s;
            animation-delay: -0.8s;
          }

          @-webkit-keyframes sk-stretchdelay {
            0%,
            40%,
            100% {
              -webkit-transform: scaleY(0.4);
            }
            20% {
              -webkit-transform: scaleY(1);
            }
          }

          @keyframes sk-stretchdelay {
            0%,
            40%,
            100% {
              transform: scaleY(0.4);
              -webkit-transform: scaleY(0.4);
            }
            20% {
              transform: scaleY(1);
              -webkit-transform: scaleY(1);
            }
          }
        `}
      </style>
    </div>
  );
};

export default LoadingIcon;
