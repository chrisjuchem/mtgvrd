import {useCallback, useState} from 'react';
import {FaChevronDown, FaChevronUp} from 'react-icons/fa';
import {Link} from 'react-router-dom';

const UserDropdown = ({username}) => {
  const [expanded, setExpanded] = useState(false);

  const toggleExpanded = useCallback(
    (override) =>
      setExpanded((wasExpanded) => {
        if (override === wasExpanded) {
          return wasExpanded;
        }

        // actually do toggle
        setTimeout(() => {
          if (wasExpanded) {
            document.body.removeEventListener('click', toggleExpanded);
          } else {
            document.body.addEventListener('click', toggleExpanded);
          }
        });
        return !wasExpanded;
      }),
    []
  );

  return (
    <div
      className={`userDropdown`}
      onBlur={(event) => {
        if (event.relatedTarget && !event.currentTarget.contains(event.relatedTarget))
          toggleExpanded(false);
      }}
    >
      <div
        tabIndex={90}
        className="nameplate navLink"
        onClick={(event) => {
          event.stopPropagation();
          toggleExpanded();
        }}
        onKeyDown={(event) => {
          if (event.key === 'Enter') toggleExpanded();
        }}
      >
        <img className="profilePic" />
        <div className="username"> {username} </div>
        <div className="chevron">{expanded ? <FaChevronUp /> : <FaChevronDown />}</div>
      </div>
      {expanded && (
        <div className="menu">
          <Link className="menuItem" to="/foo" tabIndex={91}>
            Foo
          </Link>
          <a
            className="menuItem"
            href={`/login/logout?back_to=${window.location.pathname}`}
            tabIndex={92}
          >
            Logout
          </a>
        </div>
      )}
    </div>
  );
};

export default UserDropdown;
