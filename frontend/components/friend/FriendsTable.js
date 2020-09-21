import { useState, useMemo, forwardRef } from 'react';
import { toast } from 'react-toastify';
import Table from 'react-bootstrap/Table';
import Pagination from 'react-bootstrap/Pagination';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Dropdown from 'react-bootstrap/Dropdown';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faPencilAlt,
  faTrashAlt,
  faEllipsisV,
} from '@fortawesome/free-solid-svg-icons';
import { useTable, usePagination, useGlobalFilter } from 'react-table';
import useAuth from 'contexts/auth';
import apiClient from 'services/api';
// import { wait } from 'utils/helpers';
import EditFriendModal from 'components/friend/EditFriendModal';
import ConfirmModal from 'components/widgets/ConfirmModal';

const GlobalFilter = ({ globalFilter, setGlobalFilter }) => {
  const [value, setValue] = useState(globalFilter);
  const onChange = async value => setGlobalFilter(value || undefined);
  return (
    <Form.Control
      value={value || ''}
      placeholder="Search"
      onChange={e => {
        setValue(e.target.value);
        onChange(e.target.value);
      }}
      data-test="search"
    />
  );
};

const CustomDropdownToggle = forwardRef(({ children, onClick }, ref) => (
  <div
    ref={ref}
    onClick={e => {
      e.preventDefault();
      onClick(e);
    }}
  >
    <Button variant="light" className="ellipsis-dropdown-toggle">
      {children}
    </Button>
  </div>
));

export default ({ friends }) => {
  const { fetchUser } = useAuth();
  const [selectedFriend, setSelectedFriend] = useState(null);
  const [showEditFormModal, setShowEditFormModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const deleteFriend = async () => {
    setIsDeleting(true);
    // await wait(2000);
    const { error } = await apiClient.authenticatedDelete(
      `friends/${selectedFriend.id}`
    );
    if (error) {
      console.log(error);
    } else {
      toast.success(`"${selectedFriend.name}" successfully deleted`);
      await fetchUser();
    }
    setIsDeleting(false);
    setShowDeleteModal(false);
  };

  const columns = useMemo(
    () => [
      {
        Header: 'Name',
        accessor: 'name',
      },
      {
        Header: 'Birthday',
        accessor: d => {
          const monthStr = d.date_of_birth.month.toString().padStart(2, 0);
          const dayStr = d.date_of_birth.day.toString().padStart(2, 0);
          return `${monthStr}-${dayStr}`;
        },
      },
      {
        Header: 'Age',
        accessor: 'age',
      },
      {
        Header: 'Actions',
        width: 70, // just large enough for 2 buttons with loading icon
        className: 'text-right',
        Cell: ({ row: { original } }) => {
          const friend = {
            id: original.id,
            name: original.name,
            day: original.date_of_birth.day,
            month: original.date_of_birth.month,
            year: original.date_of_birth.year,
          };
          return (
            <div className="text-right">
              <Dropdown>
                <Dropdown.Toggle as={CustomDropdownToggle} alignRight>
                  <FontAwesomeIcon icon={faEllipsisV} size={'sm'} />
                </Dropdown.Toggle>

                <Dropdown.Menu>
                  <Dropdown.Item
                    onClick={() => {
                      setSelectedFriend(friend);
                      setShowEditFormModal(true);
                    }}
                  >
                    <FontAwesomeIcon
                      icon={faPencilAlt}
                      size={'sm'}
                      style={{ marginRight: 8 }}
                    />{' '}
                    Edit
                  </Dropdown.Item>
                  <Dropdown.Item
                    onClick={() => {
                      setSelectedFriend(friend);
                      setShowDeleteModal(true);
                    }}
                  >
                    <FontAwesomeIcon
                      icon={faTrashAlt}
                      size={'sm'}
                      style={{ marginRight: 10 }}
                    />{' '}
                    Delete
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </div>
          );
        },
      },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    rows,
    page, // rows for the active page

    // global filtering helpers
    setGlobalFilter,

    // pagination helpers
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,

    // state variables
    state: { pageIndex, pageSize, globalFilter },
  } = useTable(
    {
      columns,
      data: friends,
      initialState: { pageSize: 5 },
    },
    useGlobalFilter,
    usePagination
  );

  return (
    <>
      <h4>Friends</h4>

      {rows.length === 0 ? (
        <div>Add a friend to get started</div>
      ) : (
        <>
          <EditFriendModal
            showModal={showEditFormModal}
            setShowModal={setShowEditFormModal}
            friendValues={selectedFriend}
          />

          <ConfirmModal
            showModal={showDeleteModal}
            setShowModal={setShowDeleteModal}
            onConfirm={deleteFriend}
            title={'Delete Friend?'}
            body={`Please confirm that you want to delete ${selectedFriend?.name}.`}
            confirmButtonText={'Delete'}
            isSubmitting={isDeleting}
          />

          <Row className="justify-content-between">
            <Col>
              <Form.Control
                as="select"
                value={pageSize}
                onChange={e => setPageSize(Number(e.target.value))}
                style={{ width: 120 }}
              >
                {[5, 10, 20, 40].map(size => (
                  <option key={size} value={size}>
                    Show {size}
                  </option>
                ))}
              </Form.Control>
            </Col>
            <Col xs={12} sm={6}>
              <GlobalFilter
                globalFilter={globalFilter}
                setGlobalFilter={setGlobalFilter}
              />
            </Col>
          </Row>

          <Table
            striped
            hover
            responsive
            {...getTableProps()}
            data-test="friends-table"
          >
            <thead>
              {headerGroups.map(headerGroup => (
                <tr {...headerGroup.getHeaderGroupProps()}>
                  {headerGroup.headers.map(column => {
                    return (
                      <th
                        {...column.getHeaderProps()}
                        width={column.width !== 150 ? column.width : null}
                        className=""
                      >
                        {column.render('Header')}
                      </th>
                    );
                  })}
                </tr>
              ))}
            </thead>
            <tbody {...getTableBodyProps()}>
              {page.map((row, i) => {
                prepareRow(row);
                return (
                  <tr {...row.getRowProps()}>
                    {row.cells.map(cell => {
                      return (
                        <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </Table>

          <div className="d-flex justify-content-between">
            <Pagination>
              <Pagination.First
                onClick={() => gotoPage(0)}
                disabled={!canPreviousPage}
              />
              <Pagination.Prev
                onClick={() => previousPage()}
                disabled={!canPreviousPage}
              />
              <Pagination.Next
                onClick={() => nextPage()}
                disabled={!canNextPage}
              />
              <Pagination.Last
                onClick={() => gotoPage(pageCount - 1)}
                disabled={!canNextPage}
              />
            </Pagination>
            <div>
              Page {pageIndex + 1} of {pageOptions.length || 1}{' '}
              <small className="text-muted">({rows.length} records)</small>
            </div>
          </div>
        </>
      )}
    </>
  );
};
