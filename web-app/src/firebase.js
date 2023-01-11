// // Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFunctions } from "firebase/functions";
// // TODO: Add SDKs for Firebase products that you want to use
// // https://firebase.google.com/docs/web/setup#available-libraries

// // Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA1GpTMMGXHUaQ05VxlwU_xzn7S65PoHwA",
  authDomain: "ggadot9says.firebaseapp.com",
  projectId: "ggadot9says",
  storageBucket: "ggadot9says.appspot.com",
  messagingSenderId: "91077531516",
  appId: "1:91077531516:web:954007d5c83a8940a7f6f9"
};

// // Initialize Firebase
const app = initializeApp(firebaseConfig);
const functions = getFunctions(app);
export { functions };
// const startWebSocket = functions.httpsCallable("startWebSocket");
// startWebSocket()
//   .then(response => {
//     console.log(response);
//   })
//   .catch(error => {
//     console.error(error);
//   });
