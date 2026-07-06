import { Link } from 'react-router';
import styles from './NavBar.module.css'

export default function NavBar() {

  return (
    <nav className={styles.nav}>
      <h1 className={styles.h1}>MCB</h1>
      <ul className={styles.ul}>
        <li className={styles.li}><Link to='/'>Game</Link></li>
      </ul>
      <ul className={styles.ul}>
        <li className={styles.li}><Link to='/about'>About</Link></li>
      </ul>
    </nav>

  )
}


