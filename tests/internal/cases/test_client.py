import uuid
import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from src.internal.cases.client import create, signin, get, update, delete
from src.internal.entities.client import CreateClient, SignInClient, UpdateClient
from src.db import models as m


@pytest.fixture
def mock_session():
    """Mock AsyncSession for testing."""
    session = AsyncMock(spec=AsyncSession)
    session.begin.return_value.__aenter__ = AsyncMock()
    session.begin.return_value.__aexit__ = AsyncMock(return_value=None)
    return session


@pytest.fixture
def mock_connection():
    """Mock database connection."""
    conn = AsyncMock()
    return conn


@pytest.fixture
def sample_client():
    """Sample client data for testing."""
    return m.Client(
        id=uuid.uuid4(),
        name="John",
        surname="Doe",
        email="john.doe@example.com",
        password_hash="hashed_password",
        image_url="http://example.com/image.jpg",
        tg_username="johndoe",
    )


@pytest.fixture
def create_client_data():
    """Sample CreateClient data."""
    return CreateClient(
        name="John",
        surname="Doe",
        email="john.doe@example.com",
        password="password123",
        image_url="http://example.com/image.jpg",
        tg_username="johndoe",
    )


@pytest.fixture
def signin_client_data():
    """Sample SignInClient data."""
    return SignInClient(email="john.doe@example.com", password="password123")


@pytest.fixture
def update_client_data():
    """Sample UpdateClient data."""
    return UpdateClient(
        name="Jane",
        surname=None,
        image_url="http://example.com/new_image.jpg",
        tg_username=None,
    )


class TestCreateClient:
    @pytest.mark.asyncio
    async def test_create_client_success(
        self, mock_session, sample_client, create_client_data
    ):
        # Arrange
        with patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.create_client.return_value = sample_client
            mock_querier_class.return_value = mock_querier

            # Act
            result = await create(mock_session, create_client_data)

            # Assert
            assert result == sample_client
            mock_querier.create_client.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_client_failure(self, mock_session, create_client_data):
        # Arrange
        with patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.create_client.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await create(mock_session, create_client_data)

            # Assert
            assert result is None
            mock_querier.create_client.assert_called_once()


class TestSignInClient:
    @pytest.mark.asyncio
    async def test_signin_success(
        self, mock_session, sample_client, signin_client_data
    ):
        # Arrange
        with (
            patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class,
            patch("src.internal.infra.hash.verify_password", return_value=True),
        ):
            mock_querier = AsyncMock()
            mock_querier.get_client_by_email.return_value = sample_client
            mock_querier_class.return_value = mock_querier

            # Act
            result = await signin(mock_session, signin_client_data)

            # Assert
            assert result == sample_client
            mock_querier.get_client_by_email.assert_called_once_with(
                email=signin_client_data.email
            )

    @pytest.mark.asyncio
    async def test_signin_client_not_found(self, mock_session, signin_client_data):
        # Arrange
        with patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_client_by_email.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await signin(mock_session, signin_client_data)

            # Assert
            assert result is None
            mock_querier.get_client_by_email.assert_called_once_with(
                email=signin_client_data.email
            )

    @pytest.mark.asyncio
    async def test_signin_wrong_password(
        self, mock_session, sample_client, signin_client_data
    ):
        # Arrange
        with (
            patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class,
            patch("src.internal.infra.hash.verify_password", return_value=False),
        ):
            mock_querier = AsyncMock()
            mock_querier.get_client_by_email.return_value = sample_client
            mock_querier_class.return_value = mock_querier

            # Act
            result = await signin(mock_session, signin_client_data)

            # Assert
            assert result is None
            mock_querier.get_client_by_email.assert_called_once_with(
                email=signin_client_data.email
            )


class TestGetClient:
    @pytest.mark.asyncio
    async def test_get_client_success(self, mock_session, sample_client):
        # Arrange
        client_id = sample_client.id
        with patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_client_by_id.return_value = sample_client
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get(mock_session, client_id)

            # Assert
            assert result == sample_client
            mock_querier.get_client_by_id.assert_called_once_with(id=client_id)

    @pytest.mark.asyncio
    async def test_get_client_not_found(self, mock_session):
        # Arrange
        client_id = uuid.uuid4()
        with patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_client_by_id.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get(mock_session, client_id)

            # Assert
            assert result is None
            mock_querier.get_client_by_id.assert_called_once_with(id=client_id)


class TestUpdateClient:
    @pytest.mark.asyncio
    async def test_update_client_success(
        self, mock_session, sample_client, update_client_data
    ):
        # Arrange
        client_id = sample_client.id
        updated_client = m.Client(
            id=client_id,
            name="Jane",
            surname=sample_client.surname,
            email=sample_client.email,
            password_hash=sample_client.password_hash,
            image_url="http://example.com/new_image.jpg",
            tg_username=sample_client.tg_username,
        )
        with patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.update_client.return_value = updated_client
            mock_querier_class.return_value = mock_querier

            # Act
            result = await update(mock_session, client_id, update_client_data)

            # Assert
            assert result == updated_client
            mock_querier.update_client.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_client_not_found(self, mock_session, update_client_data):
        # Arrange
        client_id = uuid.uuid4()
        with patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.update_client.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await update(mock_session, client_id, update_client_data)

            # Assert
            assert result is None
            mock_querier.update_client.assert_called_once()


class TestDeleteClient:
    @pytest.mark.asyncio
    async def test_delete_client_success(self, mock_session):
        # Arrange
        client_id = uuid.uuid4()
        with patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.delete_client.return_value = client_id
            mock_querier_class.return_value = mock_querier

            # Act
            result = await delete(mock_session, client_id)

            # Assert
            assert result is True
            mock_querier.delete_client.assert_called_once_with(id=client_id)

    @pytest.mark.asyncio
    async def test_delete_client_not_found(self, mock_session):
        # Arrange
        client_id = uuid.uuid4()
        with patch("internal.cases.client.c.AsyncQuerier") as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.delete_client.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await delete(mock_session, client_id)

            # Assert
            assert result is False
            mock_querier.delete_client.assert_called_once_with(id=client_id)

