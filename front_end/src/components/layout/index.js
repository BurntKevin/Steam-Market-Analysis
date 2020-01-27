import React from 'react';
import Header from './Header';
import Body from './Body';

function Layout({ body1, body2 }) {
  return (
    <div style={{ display: 'inline' }}>
      <Header />
      <Body>{body1}</Body>
      <Body>{body2}</Body>
    </div>
  );
}

export default Layout;
